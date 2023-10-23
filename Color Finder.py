import sys
import os
import time
from PIL import Image, ImageTk, ImageFilter
import math
import tkinter as tk
from tkinter import ttk, simpledialog, filedialog, PhotoImage
import tkinter.messagebox

size_options = {
    "1": (34, 32),
    "2": (28, 24),
    "3": (35, 33),
    "4": (24, 26),
    "5": (48, 38),
    "6": (39, 36),
    "7": (27, 24),
}

COLOR_TABLE = [
    (108, 147, 245),    # Blue Shroom
    (233, 171, 87),     # Orange Shroom
    (242, 106, 96),     # Red Shroom
    (115, 104, 199),    # Purple Shroom
    (210, 77, 33),      # Flower Red
    (67, 95, 201),      # Flower Blue
    (255, 220, 17),     # Flower Yellow
    (226, 60, 203),     # Flower Magenta
    (222, 224, 230),    # Flower White
    (255, 169, 209),    # Flower Bed Red
    (138, 224, 248),    # Flower Bed Blue
    (224, 225, 160),    # Flower Bed Green
    (28, 159, 74),      # Grass Mint
    (78, 163, 39),      # Grass Green
    (227, 192, 33),     # Grass Yellow
    (211, 113, 50),     # Grass Orange
    (33, 170, 127),     # Bush Mint
    (89, 187, 84),      # Bush Green
    (204, 113, 42),     # Bush Orange
    (195, 172, 119),    # Stam
    (228, 232, 214),    # Snowy Rock
    (216, 141, 46),     # Flower Bush Orange
    (125, 184, 42),     # Flower Bush Green
    (69, 178, 110),     # Flower Bush Mint
    (145, 150, 185),    # Symbol Rock Dark
    (185, 172, 155),    # Symbol Rock Light
    (134, 170, 142),    # Snowy Tree
    (108, 104, 99),     # Winter Tree
    (173, 131, 56),     # Snowy Spiky Tree Orange
    (73, 145, 65),      # Snowy Spiky Tree Green
    (0, 116, 124),      # Snowy Spiky Tree Mint
    (70, 143, 18),      # Bamboo
    
]

color_image_mapping = {
    (108, 147, 245): "pixel_placement_files/Blue_Shroom.png",
    (233, 171, 87): "pixel_placement_files/Orange_Shroom.png",
    (242, 106, 96): "pixel_placement_files/Red_Shroom.png",
    (115, 104, 199): "pixel_placement_files/Purple_Shroom.png",
    (210, 77, 33): "pixel_placement_files/Flower_Red.png",
    (67, 95, 201): "pixel_placement_files/Flower_Blue.png",
    (255, 220, 17): "pixel_placement_files/Flower_Yellow.png",
    (226, 60, 203): "pixel_placement_files/Flower_Magenta.png",
    (222, 224, 230): "pixel_placement_files/Flower_White.png",
    (255, 169, 209): "pixel_placement_files/Flower_Bed_Red.png",
    (138, 224, 248): "pixel_placement_files/Flower_Bed_Blue.png",
    (224, 225, 160): "pixel_placement_files/Flower_Bed_Green.png",
    (28, 159, 74): "pixel_placement_files/Grass_Mint.png",
    (78, 163, 39): "pixel_placement_files/Grass_Green.png",
    (227, 192, 33): "pixel_placement_files/Grass_Yellow.png",
    (211, 113, 50): "pixel_placement_files/Grass_Orange.png",
    (33, 170, 127): "pixel_placement_files/Bush_Mint.png",
    (89, 187, 84): "pixel_placement_files/Bush_Green.png",
    (204, 113, 42): "pixel_placement_files/Bush_Orange.png",
    (195, 172, 119): "pixel_placement_files/Stam.png",
    (228, 232, 214): "pixel_placement_files/Snowy_Rock.png",
    (216, 141, 46): "pixel_placement_files/Flower_Bush_Orange.png",
    (125, 184, 42): "pixel_placement_files/Flower_Bush_Green.png",
    (69, 178, 110): "pixel_placement_files/Flower_Bush_Mint.png",
    (145, 150, 185): "pixel_placement_files/Symbol_Rock_Dark.png",
    (185, 172, 155): "pixel_placement_files/Symbol_Rock_Light.png",
    (134, 170, 142): "pixel_placement_files/Snowy_Tree.png",
    (108, 104, 99): "pixel_placement_files/Winter_Tree.png",
    (173, 131, 56): "pixel_placement_files/Snowy_Spiky_Tree_Orange.png",
    (73, 145, 65): "pixel_placement_files/Snowy_Spiky_Tree_Green.png",
    (0, 116, 124): "pixel_placement_files/Snowy_Spiky_Tree_Mint.png",
    (70, 143, 18): "pixel_placement_files/Bamboo.png",
}

PIXEL_PLACEMENT_MAPS = {
    "1": "pixel_placement_files/34x32_pixel_placement.png", 
    "2": "pixel_placement_files/28x24_pixel_placement.png",  
    "3": "pixel_placement_files/35x33_pixel_placement.png",
    "4": "pixel_placement_files/24x26_pixel_placement.png",
    "5": "pixel_placement_files/48x38_pixel_placement.png",
    "6": "pixel_placement_files/39x36_pixel_placement.png",
    "7": "pixel_placement_files/27x24_pixel_placement.png",
}

# New function to get user input for image size and pixel placement map
def get_new_image_info():
    choice = input("Enter The Island Number: ")

    selected_size = size_options.get(choice)
    pixel_placement_map_path = PIXEL_PLACEMENT_MAPS.get(choice)

    if selected_size and pixel_placement_map_path:
        pixel_placement_map = Image.open(pixel_placement_map_path).convert('1')  # Open the image as black and white
        return selected_size, pixel_placement_map
    else:
        print("Invalid size option or missing pixel placement map.")
        return None, None

def find_closest_color(pixel, color_table):
    min_distance = float('inf')
    closest_color = None
    for color in color_table:
        distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(pixel, color)))
        if distance < min_distance:
            min_distance = distance
            closest_color = color
    return closest_color

class SizeSelectionApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Size Selection")
        self.geometry("600x500")
        self.selected_size = None
        self.image_processed = False  # Flag to track if image processing is done
        row_num = 1  # Initialize row_num here

        label = tk.Label(self, text="Select Size:")
        label.grid(row=0, column=0, padx=10, pady=20)

        row_num = 1
        for size in size_options.keys():
            button = tk.Button(self, text=size, width=10, height=2, command=lambda s=size: self.on_size_selected(s))
            button.grid(row=row_num, column=0, padx=10, pady=10, sticky="w")
            row_num += 1

        # Load and keep a reference to the background image
        image_path = "pixel_placement_files/background.png"
        self.background_image = Image.open(image_path)
        self.background_image = ImageTk.PhotoImage(self.background_image)

        # Display the background image using a label
        background_label = tk.Label(self, image=self.background_image)
        background_label.image = self.background_image  # Keep a reference to avoid garbage collection
        background_label.grid(row=1, column=1, padx=10, pady=20, rowspan=row_num)

    def on_size_selected(self, size):
        self.selected_size = size
        self.process_selected_image()

    def process_selected_image(self):
        if self.selected_size:
            file_path = filedialog.askopenfilename(title="Select a 64x64 image",
                                                   filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
            if file_path:
                width, height = size_options.get(self.selected_size, (0, 0))
                pixel_placement_map_path = PIXEL_PLACEMENT_MAPS.get(self.selected_size)
                pixel_placement_map = Image.open(pixel_placement_map_path).convert('1')
                self.process_image(file_path, (width, height), pixel_placement_map)

    def show_done_message(self):
        # Display a "done" message box
        tkinter.messagebox.showinfo("Done", "Image processing is complete!")

    def process_image_with_delay(self, image_path, new_size, pixel_placement_map):
    # Schedule the image processing after a delay
        self.after(100, self.process_image, image_path, new_size, pixel_placement_map)


    def show_processed_image(self, output_image_path):
        processed_image_window = tk.Toplevel(self)
        processed_image_window.title("Processed Image")
        processed_image_window.attributes('-topmost', True)  # Set the window to be on top
        processed_image_window.configure(bg='black')  # Set the background color to black

        processed_image = Image.open(output_image_path).convert('RGBA')
        processed_image = processed_image.resize((600, 600), Image.NEAREST)  # Resize using nearest-neighbor interpolation

        processed_image_tk = ImageTk.PhotoImage(processed_image)

        processed_image_label = tk.Label(processed_image_window, image=processed_image_tk, bg='black')
        processed_image_label.image = processed_image_tk
        processed_image_label.pack(padx=10, pady=20)

    def process_image(self, image_path, new_size, pixel_placement_map):
        image = Image.open(image_path).convert('RGBA')

        # Resize the image using nearest-neighbor interpolation
        image = image.resize(new_size, Image.NEAREST)

        # Create an output image that is 25 times larger
        output_image_size = (new_size[0] * 25, new_size[1] * 25)
        output_image = Image.new('RGBA', output_image_size)

        total_pixels = output_image_size[0] * output_image_size[1]
        processed_pixels = 0

        # Ask the user if they want to overlay the images
        overlay_images = tkinter.messagebox.askyesno("Overlay Images", "Do you want to overlay images? it will be faster without, but also harder to understand which pixel is which object.")
    
        for y in range(output_image_size[1]):
            for x in range(output_image_size[0]):
                # Map the current output pixel coordinates back to the original size
                original_x = x // 25
                original_y = y // 25

                if original_x < pixel_placement_map.width and original_y < pixel_placement_map.height and \
                        pixel_placement_map.getpixel((original_x, original_y)) == 255:
                    pixel = image.getpixel((original_x, original_y))
                    r, g, b, a = pixel

                    if a == 0:
                        output_image.putpixel((x, y), (0, 0, 0, 0))
                    else:
                        closest_color = find_closest_color((r, g, b), COLOR_TABLE)
                        # Overlay pixel with corresponding image
                        if closest_color in color_image_mapping and overlay_images:
                            overlay_img_path = color_image_mapping[closest_color]
                            overlay_img = Image.open(overlay_img_path).convert('RGBA')
                            overlay_img = overlay_img.resize((25, 25), Image.NEAREST)
                            final_pixel = (
                                int((1 - a / 255) * r + a / 255 * overlay_img.getpixel((x % 25, y % 25))[0]),
                                int((1 - a / 255) * g + a / 255 * overlay_img.getpixel((x % 25, y % 25))[1]),
                                int((1 - a / 255) * b + a / 255 * overlay_img.getpixel((x % 25, y % 25))[2]),
                                a
                            )
                            output_image.putpixel((x, y), final_pixel)
                        else:
                            output_image.putpixel((x, y), closest_color + (a,))

        # Save the processed image
        output_image_path = 'output_image.png'
        output_image.save(output_image_path)
        print("finished")
        self.show_processed_image(output_image_path)  # Display the processed image
        self.show_done_message()
        self.image_processed = True  # Set the flag to indicate image processing is done

    def on_closing(self):
        if not self.image_processed:
            # If image processing is not done, show a warning message before closing
            if tkinter.messagebox.askokcancel("Quit", "Image processing is not complete. Are you sure you want to quit?"):
                self.destroy()
        else:
            self.destroy()  # Close the window directly if image processing is done


if __name__ == "__main__":
    app = SizeSelectionApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)  # Bind the closing event to the on_closing method
    app.mainloop()

    # Select Image
    root = tk.Tk()
    root.withdraw()  # Hide Window
    root.mainloop()  # Keep the tkinter main loop running
