#!/usr/bin/env python3
"""Create an animated GIF from ASCII grid files."""

import glob
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def extract_number(filename):
    """Extract the iteration number from filename."""
    match = re.search(r'grid_iteration_(\d+)\.txt', filename)
    return int(match.group(1)) if match else float('inf')

def create_gif(output_filename='animation.gif', duration=100, font_size=8):
    """
    Create an animated GIF from grid_iteration_*.txt files.
    
    Args:
        output_filename: Name of the output GIF file
        duration: Duration of each frame in milliseconds
        font_size: Size of the monospace font for ASCII rendering
    """
    # Get all grid files and sort by iteration number
    grid_files = sorted(
        glob.glob('grid_iteration_*.txt'),
        key=extract_number
    )
    
    if not grid_files:
        print("No grid_iteration_*.txt files found!")
        return
    
    print(f"Found {len(grid_files)} grid files")
    
    # Try to use a monospace font, fall back to default if not available
    try:
        font = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", font_size)
    except:
        print("Warning: Could not load monospace font, using default")
        font = ImageFont.load_default()
    
    frames = []
    
    for i, grid_file in enumerate(grid_files):
        print(f"Processing {grid_file} ({i+1}/{len(grid_files)})")
        
        with open(grid_file, 'r') as f:
            lines = f.readlines()
        
        # Remove empty lines and strip trailing whitespace
        lines = [line.rstrip('\n') for line in lines if line.strip()]
        
        if not lines:
            continue
        
        # Calculate image dimensions
        # Use character-based dimensions with monospace font
        char_width = 6  # Approximate width of a character at font_size 8
        char_height = 10  # Approximate height of a character at font_size 8
        
        max_width = max(len(line) for line in lines) if lines else 1
        height = len(lines)
        
        img_width = max_width * char_width + 20  # Add padding
        img_height = height * char_height + 20
        
        # Create image with white background
        img = Image.new('RGB', (img_width, img_height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw the ASCII grid
        for y, line in enumerate(lines):
            draw.text(
                (10, 10 + y * char_height),
                line,
                fill='black',
                font=font
            )
        
        frames.append(img)
    
    if not frames:
        print("No frames were created!")
        return
    
    print(f"Creating GIF with {len(frames)} frames...")
    
    # Save as animated GIF
    frames[0].save(
        output_filename,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0  # Loop forever
    )
    
    print(f"Animation saved to {output_filename}")

if __name__ == '__main__':
    create_gif()
