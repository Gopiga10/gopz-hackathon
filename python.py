mport tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import requests

# Replace with your actual API key
API_KEY = 'AIzaSyBg4bmC3Uvvsls90rOvhhBFZOzWnrrc_0A'
API_ENDPOINT = 'https://api.geminivisionpro.com/v1/process'

class SimpleApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Simple Image Processor")

        # Widgets
        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        self.text_entry = tk.Entry(root, width=50)
        self.text_entry.pack(pady=10)

        self.process_button = tk.Button(root, text="Process Image", command=self.process_image)
        self.process_button.pack(pady=10)

        self.image_path = None

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", ".png;.jpg;*.jpeg")])
  if self.image_path:
            image = Image.open(self.image_path)
            image.thumbnail((250, 250))
            photo = ImageTk.PhotoImage(image)

            if hasattr(self, 'image_label'):
                self.image_label.config(image=photo)
                self.image_label.image = photo
            else:
                self.image_label = tk.Label(self.root, image=photo)
                self.image_label.photo = photo
                self.image_label.pack(pady=10)

    def process_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please upload an image first.")
            return

        user_text = self.text_entry.get()
        if not user_text:
            messagebox.showerror("Error", "Please enter text.")
            return

        try:
            with open(self.image_path, 'rb') as img_file:
                files = {'image': ('file.jpg', img_file, 'image/jpeg')}
                data = {'text': user_text}  # Adjust based on API requirements
                headers = {'x-api-key': API_KEY}
                response = requests.post(API_ENDPOINT, files=files, data=data, headers=headers)
                response.raise_for_status()
                result = response.json()
                messagebox.showinfo("Result", f"Response: {result}")

        except requests.RequestException as e:
            messagebox.showerror("Error", f"API error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if _name_ == "_main_":
    root = tk.Tk()
    app = SimpleApp(root)
    root.mainloop()
