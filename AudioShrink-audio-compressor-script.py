#!/usr/bin/env python3
"""
Dynamic Audio Compression Script

This script compresses audio files to a specified target size by dynamically
calculating the appropriate bitrate. It works with various audio formats
including m4a, wav, mp3, etc., and outputs compressed mp3 files.

Usage:
    python compress_audio.py input_file output_file [target_size_mb]

Example:
    python compress_audio.py large_audio.m4a compressed_audio.mp3 180
"""

import os
import sys
import argparse
import math
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from pydub import AudioSegment


def get_file_size_mb(file_path):
    """Get file size in megabytes"""
    return os.path.getsize(file_path) / (1024 * 1024)


def get_audio_duration(file_path):
    """Get audio duration in seconds using pydub"""
    audio = AudioSegment.from_file(file_path)
    return len(audio) / 1000  # Convert milliseconds to seconds


def calculate_bitrate(input_size_mb, duration_seconds, target_size_mb=199):
    """
    Calculate the appropriate bitrate to achieve target file size
    
    Args:
        input_size_mb: Size of input file in MB
        duration_seconds: Duration of audio in seconds
        target_size_mb: Target file size in MB (default: 199)
        
    Returns:
        Appropriate bitrate in kbps as an integer
    """
    # Convert MB to bits
    input_size_bits = input_size_mb * 8 * 1024 * 1024
    target_size_bits = target_size_mb * 8 * 1024 * 1024
    
    # Calculate original bitrate
    original_bitrate = input_size_bits / duration_seconds
    
    # Calculate target bitrate (bits per second)
    target_bitrate = target_size_bits / duration_seconds
    
    # Convert to kbps for standard audio bitrates
    target_kbps = target_bitrate / 1000
    
    # Standard MP3 bitrates (kbps)
    standard_bitrates = [320, 256, 192, 160, 128, 112, 96, 80, 64, 48, 32]
    
    # Find the highest standard bitrate that's below our target
    for bitrate in standard_bitrates:
        if bitrate <= target_kbps:
            return bitrate
    
    # If no standard bitrate is low enough, return the lowest
    return standard_bitrates[-1]


def compress_audio(input_file, output_file, target_bitrate):
    """
    Compress audio file to target bitrate
    
    Args:
        input_file: Path to input audio file
        output_file: Path to save output file
        target_bitrate: Bitrate in kbps to use for compression
        
    Returns:
        Tuple of (input_size_mb, output_size_mb)
    """
    print(f"Compressing {input_file} with bitrate {target_bitrate}kbps...")
    
    # Load the audio file
    audio = AudioSegment.from_file(input_file)
    
    # Export with the specified bitrate
    audio.export(output_file, format="mp3", bitrate=f"{target_bitrate}k")
    
    # Get file sizes
    input_size = get_file_size_mb(input_file)
    output_size = get_file_size_mb(output_file)
    
    return input_size, output_size


def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Compress audio files to a target size')
    parser.add_argument('input_file', help='Path to the input audio file')
    parser.add_argument('output_file', nargs='?', help='Path to save the compressed output file (default: same as input with .mp3 extension)')
    parser.add_argument('target_size', type=float, nargs='?', default=199, 
                        help='Target size in MB (default: 199)')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.isfile(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.")
        return 1
        
    # Set default output file if not specified
    if not args.output_file:
        # Extract the directory and filename from the input path
        input_dir = os.path.dirname(args.input_file)
        input_filename = os.path.basename(args.input_file)
        
        # Remove the extension and add .mp3
        base_name = os.path.splitext(input_filename)[0]
        output_filename = f"{base_name}.mp3"
        
        # Combine directory with new filename
        if input_dir:
            args.output_file = os.path.join(input_dir, output_filename)
        else:
            args.output_file = output_filename
            
        print(f"No output file specified. Using: {args.output_file}")
    
    try:
        # Get input file size
        input_size = get_file_size_mb(args.input_file)
        print(f"Input file size: {input_size:.2f} MB")
        
        # Check if input is already smaller than target
        if input_size < args.target_size:
            print(f"Input file is already smaller than target size ({args.target_size:.2f} MB)")
            print(f"Copying file to {args.output_file} without compression...")
            audio = AudioSegment.from_file(args.input_file)
            audio.export(args.output_file, format="mp3", bitrate="320k")
            output_size = get_file_size_mb(args.output_file)
            print(f"Output file size: {output_size:.2f} MB")
            return 0
        
        # Get audio duration
        print("Analyzing audio duration...")
        duration = get_audio_duration(args.input_file)
        print(f"Audio duration: {duration:.2f} seconds ({duration/60:.2f} minutes)")
        
        # Calculate target bitrate
        bitrate = calculate_bitrate(input_size, duration, args.target_size)
        print(f"Calculated target bitrate: {bitrate} kbps")
        
        # Compress the audio
        input_size, output_size = compress_audio(args.input_file, args.output_file, bitrate)
        
        # Print results
        print("\nCompression Results:")
        print(f"Input file: {args.input_file} ({input_size:.2f} MB)")
        print(f"Output file: {args.output_file} ({output_size:.2f} MB)")
        print(f"Compression ratio: {input_size/output_size:.2f}x")
        print(f"Used bitrate: {bitrate} kbps")
        
        # Check if we achieved target size
        if output_size < args.target_size:
            print(f"Success! Output file is {args.target_size - output_size:.2f} MB below target.")
            return 0
        else:
            print(f"Warning: Output file is {output_size - args.target_size:.2f} MB above target size.")
            print("Consider using a lower bitrate manually.")
            return 1
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())