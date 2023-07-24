import os
from PIL import Image, ImageDraw
import argparse
import datetime

def generate_calibration_image_1(output_file, resolution):

    width, height = resolution
    image = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Calculate bar heights
    bar_height_1 = int(height * (8 / 12))
    bar_height_2 = int(height * (1 / 12))
    bar_height_3 = int(height * (3 / 12))
    
    # Colors for the rows
    row1_colors = [(204, 204, 204), (255, 255, 0), (0, 255, 255), (0, 255, 0), (255, 0, 255), (255, 0, 0), (0, 0, 255)]
    row2_colors = [(0, 0, 255), (19, 19, 19), (255, 0, 255), (19, 19, 19), (0, 255, 255), (19, 19, 19), (204, 204, 204)]
    row3_colors = [(8, 62, 89), (255, 255, 255), (58, 0, 126), (19, 19, 19), (0, 0, 0), (19, 19, 19), (38, 38, 38), (19, 19, 19)]

    # Draw the first row color bars
    x_position = 0
    row1_widths = [23/160*width]*6 + [11/80*width]
    for i, color in enumerate(row1_colors):
        draw.rectangle([(x_position, 0), (x_position + row1_widths[i], bar_height_1)], fill=color)
        x_position += row1_widths[i]
    
    # Draw the second row color bars
    x_position = 0
    row2_widths = [23/160*width]*6 + [11/80*width]
    for i, color in enumerate(row2_colors):
        draw.rectangle([(x_position, bar_height_1), (x_position + row2_widths[i], bar_height_1 + bar_height_2)], fill=color)
        x_position += row2_widths[i]
    
    # Draw the third row color bars
    x_position = 0
    row3_widths = [7/40*width, 7/40*width, 7/40*width, 31/160*width, 7/160*width, 1/20*width, 1/20*width, 11/80*width]
    for i, color in enumerate(row3_colors):
        draw.rectangle([(x_position, bar_height_1 + bar_height_2), (x_position + row3_widths[i], height)], fill=color)
        x_position += row3_widths[i]
    
    image.save(output_file)
    
def generate_calibration_image_2(output_file, resolution):
    
    width, height = resolution
    image = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Calculate bar heights
    bar_height = int(height * (1 / 7))
    
    # Colors for the rows
    colors = [(1023, 1023, 1023),    # Row 1: Black to white gradient
              (1023, 0, 0),          # Row 2: Red to black gradient
              (0, 1023, 0),          # Row 3: Black to green gradient
              (0, 0, 1023),          # Row 4: Blue to black gradient
              (1023, 1023, 0),       # Row 5: Black to yellow gradient
              (0, 1023, 1023),       # Row 6: Cyan to black gradient
              (1023, 0, 1023)]       # Row 7: Black to pink gradient

    # Draw the gradient rows
    y_position = 0
    for i, color in enumerate(colors):
        if i == 1 or i == 3 or i == 5:
            for j in range(width):
                r = int(((width - j) / width) * color[0])
                g = int(((width - j) / width) * color[1])
                b = int(((width - j) / width) * color[2])
                draw.line((j, y_position, j, y_position + bar_height), fill=(r //4 , g //4 , b //4))
        else:
            for j in range(width):
                r = int((color[0] / width) * j)
                g = int((color[1] / width) * j)
                b = int((color[2] / width) * j)
                draw.line((j, y_position, j, y_position + bar_height), fill=(r //4 , g //4 , b //4))
        y_position += bar_height

    image.save(output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a color TV calibration image.')
    parser.add_argument('--resolution', type=int, nargs=2, default=[1920, 1080], help='Output resolution of the image (width height)')
    parser.add_argument('--filetype', type=str, default='png', help='File type for the calibration image (png or jpg)')
    args = parser.parse_args()
                            
    script_dir = os.path.dirname(os.path.abspath(__file__))
    renders_dir = os.path.join(script_dir, 'renders')
    os.makedirs(renders_dir, exist_ok=True)
    
    date_str = datetime.datetime.now().strftime('%y%m%d')
    output_file_1 = os.path.join(renders_dir, f'calibration_0001_{args.resolution[0]}x{args.resolution[1]}_{date_str}.{args.filetype}')
    output_file_2 = os.path.join(renders_dir, f'calibration_0002_{args.resolution[0]}x{args.resolution[1]}_{date_str}.{args.filetype}')
    
    generate_calibration_image_1(output_file_1, args.resolution)
    generate_calibration_image_2(output_file_2, args.resolution)
