import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import PyPDF2
import os

class PDFEditor:
    def __init__(self):
        pass
    
    def remove_pages(self, input_pdf, output_pdf, pages_to_remove):
        try:
            with open(input_pdf, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                writer = PyPDF2.PdfWriter()
                
                total_pages = len(reader.pages)
                for page_num in range(total_pages):
                    if page_num not in pages_to_remove:
                        writer.add_page(reader.pages[page_num])
                with open(output_pdf, 'wb') as output_file:
                    writer.write(output_file)
                
                return True
                
        except FileNotFoundError:
            return False
        except Exception as e:
            return False
    
    def join_pdfs(self, pdf_list, output_pdf):
        try:
            writer = PyPDF2.PdfWriter()
            
            for pdf_file in pdf_list:
                if not os.path.exists(pdf_file):
                    continue
                
                with open(pdf_file, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    for page in reader.pages:
                        writer.add_page(page)
            
            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)
            return True
            
        except Exception as e:
            return False
    
    def extract_page(self, input_pdf, output_pdf, page_number):
        try:
            with open(input_pdf, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                if page_number >= len(reader.pages) or page_number < 0:
                    return False
                
                writer = PyPDF2.PdfWriter()
                writer.add_page(reader.pages[page_number])
                
                with open(output_pdf, 'wb') as output_file:
                    writer.write(output_file)
                
                return True
                
        except FileNotFoundError:
            return False
        except Exception as e:
            return False
    
    def get_pdf_info(self, pdf_file):
        try:
            with open(pdf_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                return num_pages
                
        except FileNotFoundError:
            return 0
        except Exception as e:
            return 0
    
    def compress_pdf(self, input_pdf, output_pdf):
        try:
            original_size = os.path.getsize(input_pdf)
            
            with open(input_pdf, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                writer = PyPDF2.PdfWriter()
                
                for page in reader.pages:
                    page.compress_content_streams()
                    writer.add_page(page)
                
                with open(output_pdf, 'wb') as output_file:
                    writer.write(output_file)
                
                compressed_size = os.path.getsize(output_pdf)
                reduction = ((original_size - compressed_size) / original_size) * 100
                
                return True, original_size, compressed_size, reduction
                
        except FileNotFoundError:
            return False, 0, 0, 0
        except Exception as e:
            return False, 0, 0, 0


class PDFEditorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📄 PDF Editor - Desktop App")
        self.root.geometry("500x600")
        self.root.configure(bg="#f0f0f0")
        
        self.editor = PDFEditor()
        
        self.create_widgets()
    
    def create_widgets(self):
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X)
        
        title = tk.Label(
            title_frame, 
            text="PDF Editor",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title.pack(pady=15)
        
        subtitle = tk.Label(
            title_frame,
            text="Choose an operation",
            font=("Arial", 12),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        subtitle.pack(pady=5)
        
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.button_style = {"font": ("Arial", 11, "bold"), "height": 2, "width": 25}
        
        buttons = [
            ("Get PDF Info", self.on_get_info_clicked, "#3498db"),
            ("Remove Pages", self.on_remove_pages_clicked, "#e74c3c"),
            ("Extract Page", self.on_extract_page_clicked, "#2ecc71"),
            ("Join PDFs", self.on_join_pdfs_clicked, "#f39c12"),
            ("Compress PDF", self.on_compress_pdf_clicked, "#9b59b6"),
            ("Exit", self.root.quit, "#34495e")
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                bg=color,
                fg="white",
                **self.button_style,
                cursor="hand2",
                relief=tk.RAISED,
                bd=2
            )
            btn.pack(pady=10)
    
    def on_get_info_clicked(self):
        pdf_file = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        
        if not pdf_file:
            return
        
        num_pages = self.editor.get_pdf_info(pdf_file)
        
        if num_pages > 0:
            messagebox.showinfo(
                "PDF Information",
                f"File: {os.path.basename(pdf_file)}\nTotal Pages: {num_pages}"
            )
        else:
            messagebox.showerror("Error", "Could not read PDF file")
    
    def on_remove_pages_clicked(self):
        input_pdf = filedialog.askopenfilename(
            title="Select PDF to remove pages from",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if not input_pdf:
            return
        
        pages_str = simpledialog.askstring(
            "Remove Pages",
            "Enter page numbers to remove (comma-separated, e.g., 0,2,5)\nNote: First page is 0"
        )
        
        if not pages_str:
            return
        
        try:
            pages_to_remove = [int(p.strip()) for p in pages_str.split(",")]
        except ValueError:
            messagebox.showerror("Error", "Please enter valid page numbers")
            return
        
        output_pdf = filedialog.asksaveasfilename(
            defaultext=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if not output_pdf:
            return
        
        if self.editor.remove_pages(input_pdf, output_pdf, pages_to_remove):
            messagebox.showinfo("Success", f"Pages removed successfully!\nSaved to:\n{output_pdf}")
        else:
            messagebox.showerror("Error", "Failed to remove pages")
    
    def on_extract_page_clicked(self):
        input_pdf = filedialog.askopenfilename(
            title="Select PDF to extract from",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if not input_pdf:
            return
        
        num_pages = self.editor.get_pdf_info(input_pdf)
        if num_pages == 0:
            messagebox.showerror("Error", "Could not read PDF")
            return
        
        page_str = simpledialog.askstring(
            "Extract Page",
            f"Enter page number to extract (0-{num_pages-1})\nNote: First page is 0"
        )
        
        if not page_str:
            return
        
        try:
            page_num = int(page_str)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid page number")
            return
        
        output_pdf = filedialog.asksaveasfilename(
            defaultext=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if not output_pdf:
            return
        
        if self.editor.extract_page(input_pdf, output_pdf, page_num):
            messagebox.showinfo("Success", f"Page extracted successfully!\nSaved to:\n{output_pdf}")
        else:
            messagebox.showerror("Error", "Failed to extract page")
    
    def on_join_pdfs_clicked(self):
        pdf_list = filedialog.askopenfilenames(
            title="Select PDFs to join (select multiple files)",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if not pdf_list or len(pdf_list) < 2:
            messagebox.showerror("Error", "Please select at least 2 PDFs")
            return
        
        output_pdf = filedialog.asksaveasfilename(
            defaultext=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if not output_pdf:
            return
        
        if self.editor.join_pdfs(list(pdf_list), output_pdf):
            messagebox.showinfo("Success", f"PDFs joined successfully!\nSaved to:\n{output_pdf}")
        else:
            messagebox.showerror("Error", "Failed to join PDFs")
    
    def on_compress_pdf_clicked(self):
        input_pdf = filedialog.askopenfilename(
            title="Select PDF to compress",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if not input_pdf:
            return
        
        output_pdf = filedialog.asksaveasfilename(
            defaultext=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if not output_pdf:
            return
        
        success, original_size, compressed_size, reduction = self.editor.compress_pdf(input_pdf, output_pdf)
        
        if success:
            msg = (
                f"PDF compressed successfully!\n\n"
                f"Original size: {original_size / 1024:.2f} KB\n"
                f"Compressed size: {compressed_size / 1024:.2f} KB\n"
                f"Reduction: {reduction:.1f}%\n\n"
                f"Saved to:\n{output_pdf}"
            )
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", "Failed to compress PDF")


if __name__ == "__main__":
    root = tk.Tk()
    gui = PDFEditorGUI(root)
    root.mainloop()
