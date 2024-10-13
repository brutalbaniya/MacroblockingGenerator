import os
import cv2
import numpy as np

def shift_pixels_in_block(block, shift_value):
    """
    Applies random shifts within the block, using variable shifts in both x and y directions.
    """
    height, width = block.shape[:2]
    shifted_block = block.copy()

    # Shift pixels inside the block using small random shifts
    for y in range(height):
        for x in range(width):
            shift_x = np.random.randint(-shift_value, shift_value + 1)
            shift_y = np.random.randint(-shift_value, shift_value + 1)

            new_x = min(max(x + shift_x, 0), width - 1)
            new_y = min(max(y + shift_y, 0), height - 1)

            shifted_block[y, x] = block[new_y, new_x]

    return shifted_block


def shift_pixels_in_block_directional(block, shift_value, direction):
    """
    Shifts pixels within the block in a specific direction.
    The `direction` parameter determines the shift direction.
    Directions:
        'up'    - shifts pixels upwards
        'down'  - shifts pixels downwards
        'left'  - shifts pixels to the left
        'right' - shifts pixels to the right
    """
    height, width = block.shape[:2]
    shifted_block = block.copy()

    if direction == 'up':
        for y in range(height):
            for x in range(width):
                new_y = max(y - shift_value, 0)
                shifted_block[y, x] = block[new_y, x]
    
    elif direction == 'down':
        for y in range(height):
            for x in range(width):
                new_y = min(y + shift_value, height - 1)
                shifted_block[y, x] = block[new_y, x]

    elif direction == 'left':
        for y in range(height):
            for x in range(width):
                new_x = max(x - shift_value, 0)
                shifted_block[y, x] = block[y, new_x]

    elif direction == 'right':
        for y in range(height):
            for x in range(width):
                new_x = min(x + shift_value, width - 1)
                shifted_block[y, x] = block[y, new_x]

    return shifted_block


def copy_from_middle(frame, x, y, block_size, padding_margin):
    """
    Copies pixels from the middle region of the image to avoid copying from the edges or background.
    Adds padding to ensure copied pixels are within a safe region.
    """
    height, width = frame.shape[:2]

    
    middle_x_start = padding_margin
    middle_x_end = width - padding_margin
    middle_y_start = padding_margin
    middle_y_end = height - padding_margin

    
    middle_x = np.random.randint(middle_x_start, middle_x_end - block_size)
    middle_y = np.random.randint(middle_y_start, middle_y_end - block_size)

    
    return frame[middle_y:middle_y + block_size, middle_x:middle_x + block_size]

def resize_block_if_needed(block, target_height, target_width):
    """
    Resizes the block if the dimensions do not match the target size.
    """
    block_height, block_width = block.shape[:2]
    if block_height != target_height or block_width != target_width:
        return cv2.resize(block, (target_width, target_height), interpolation=cv2.INTER_LINEAR)
    return block


def create_checkered_pattern_with_padding(frame, block_size, max_shift_value, padding_margin, blend_factor, horizontal=True):
    height, width = frame.shape[:2]
    modified_frame = frame.copy()

    if horizontal:
        
        top_half = frame[0:height // 2, :]
        bottom_half = frame[height // 2:, :]

        
        for y in range(0, height // 2, block_size):
            for x in range(0, width, block_size):
                if (x // block_size + y // block_size) % 2 == 0:
                    # Copy from the middle region of the top half to avoid background
                    block_width = min(block_size, width - x)
                    block_height = min(block_size, (height // 2) - y)

                    middle_block = copy_from_middle(top_half, x, y, block_size, padding_margin)
                    
                    
                    middle_block = resize_block_if_needed(middle_block, block_height, block_width)

                    
                    shifted_block = shift_pixels_in_block(middle_block, max_shift_value)

                    
                    bottom_block = frame[height // 2 + y:height // 2 + y + block_height, x:x + block_width]
                    bottom_block = resize_block_if_needed(bottom_block, block_height, block_width)

                    blended_block = cv2.addWeighted(bottom_block, 1 - blend_factor, shifted_block, blend_factor, 0)

                    # Assign the blended block back to the modified frame
                    modified_frame[height // 2 + y:height // 2 + y + block_height, x:x + block_width] = blended_block
    else:
        # Split the image into left and right halves
        left_half = frame[:, 0:width // 2]
        right_half = frame[:, width // 2:]

        
        for y in range(0, height, block_size):
            for x in range(0, width // 2, block_size):
                if (x // block_size + y // block_size) % 2 == 0:
                    
                    block_width = min(block_size, (width // 2) - x)
                    block_height = min(block_size, height - y)

                    middle_block = copy_from_middle(left_half, x, y, block_size, padding_margin)
                    
                    
                    middle_block = resize_block_if_needed(middle_block, block_height, block_width)

                   
                    shifted_block = shift_pixels_in_block_directional(middle_block, shift_value, direction) #shift_pixels_in_block(middle_block, max_shift_value)

                   
                    right_block = frame[y:y + block_height, width // 2 + x:width // 2 + x + block_width]
                    right_block = resize_block_if_needed(right_block, block_height, block_width)

                    blended_block = cv2.addWeighted(right_block, 1 - blend_factor, shifted_block, blend_factor, 0)

                    # Assign the blended block back to the modified frame
                    modified_frame[y:y + block_height, width // 2 + x:width // 2 + x + block_width] = blended_block

    return modified_frame


def process_frames_with_middle_copying(input_folder, output_folder, block_size, max_shift_value, padding_margin, blend_factor, direction ,horizontal=True):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.png'):
            frame = cv2.imread(os.path.join(input_folder, filename))
            frame = create_checkered_pattern_with_padding(frame, block_size, max_shift_value, padding_margin, blend_factor, horizontal)

            cv2.imwrite(os.path.join(output_folder, filename), frame)

# Example usage
#process_frames_with_middle_copying('frames', 'modified_frames_with_directions', 24, 100, 100, 0.4, 'left', True)
