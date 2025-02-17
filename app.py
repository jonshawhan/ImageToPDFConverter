import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from reportlab.pdfgen import canvas
from PIL import Image
import os
# TODO: add a feature to select the output directory for the PDF file
# TODO: add a feature to show the user the progress of the conversion process with a progress bar
# TODO: dockerize the application
# TODO: turn this dockerized script into an executable


class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.image_paths = []
        self.output_pdf_name = tk.StringVar()
        self.selected_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=50)
        
        self.initialize_ui()
        
    def initialize_ui(self):
        title_label = tk.Label(self.root, text="Image to PDF Converter", font=("Times New Roman", 16, "bold"))
        title_label.pack(pady=10)
        
        select_images_button = tk.Button(self.root, text="Select Images", command=self.select_images)
        select_images_button.pack(pady=(0, 10))
        
        self.selected_images_listbox.pack(pady=(0, 10), fill=tk.BOTH, expand=True)
        
        label = tk.Label(self.root, text="Output PDF Name")
        label.pack()
        
        pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, width=40, justify='center')
        pdf_name_entry.pack()
        
        convert_button = tk.Button(self.root, text="Convert to PDF", command=self.convert_images_to_pdf)
        convert_button.pack(pady=(20, 40))
    
    def select_images(self):
        self.image_paths = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        self.update_selected_images_listbox()
        
    def update_selected_images_listbox(self):
        self.selected_images_listbox.delete(0, tk.END)
        
        for image_path in self.image_paths:
            _, filename = os.path.split(image_path)
            self.selected_images_listbox.insert(tk.END, filename)
           
    def convert_images_to_pdf(self):
        if not self.image_paths:
            messagebox.showerror("Error", "No images selected.")
            return
        
        output_pdf_path = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else "output.pdf"
        
        pdf = canvas.Canvas(output_pdf_path, pagesize=(612, 792))
        
        for image_path in self.image_paths:
            try:
                img = Image.open(image_path)
                available_width, available_height = 540, 720
                scale_factor = min(available_width / img.width, available_height / img.height)
                new_width = img.width * scale_factor
                new_height = img.height * scale_factor
                x_centered = (612 - new_width) / 2
                y_centered = (792 - new_height) / 2
                
                pdf.setFillColorRGB(1, 1, 1)
                pdf.rect(0, 0, 612, 792, fill=True)
                pdf.drawInlineImage(image_path, x_centered, y_centered, width=new_width, height=new_height)
                pdf.showPage()
            except Exception as e:
                messagebox.showerror("Error", f"Error processing {image_path}: {e}")
            
        pdf.save()
        
        messagebox.showinfo("Success", "File converted successfully!")
        
def main():
    root = tk.Tk()
    root.title("Image to PDF")
    converter = ImageToPDFConverter(root)
    root.geometry("400x600")
    root.mainloop()

if __name__ == "__main__":
    main()