from fpdf import FPDF
from PIL import Image
import os
import sys
import getopt

pdf = FPDF()
imagelist = []  # Contains the list of all images to be converted to PDF.

help_text = {
    'usage_cmd_single': 'jpg2pdf -s <source_image>',
    'usage_cmd_folder': 'jpg2pdf -f <source_images_folder> -n <output_pdf_name> -e <source_image_extension>',
    'usage_text': '\n123',
    'about': '\nSimple Python script to create a PDF file from a set of images\n\nSource code: https://github.com/lgg/jpg2pdf',
}

# TODO: add flags: j for JPG/jfif/JPEG and p for PNG instead of -e
# TODO: add wrong input command parser
# TODO: add -s flag for single file
# TODO: fix all text output
# TODO: check what happen when send horizontal images
# TODO: add flag for vertical/horizontal orientation

# --------------- USER INPUT -------------------- #

folder = ""  # Folder containing all the images.
name = ""
extension = ""  # Name of the output PDF file.


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hf:n:e:", ["folder=", "name=", "extension="])
    except getopt.GetoptError:
        print(help_text['usage_cmd'])
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print(help_text['usage_cmd'])
            print(help_text['usage_text'])
            print(help_text['about'])
            sys.exit()
        elif opt in ("-f", "--folder"):
            folder = arg
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-e", "--extension"):
            extension = arg

    # ------------- ADD ALL THE IMAGES IN A LIST ------------- #
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in [f for f in filenames if f.endswith(extension) or f.lower().endswith(extension)]:
            full_path = os.path.join(dirpath, filename)
            imagelist.append(full_path)

    imagelist.sort() # Sort the images by name.
    for i in range(0, len(imagelist)):
        print(imagelist[i])

    # --------------- ROTATE ANY LANDSCAPE MODE IMAGE IF PRESENT ----------------- #

    for i in range(0, len(imagelist)):
        im1 = Image.open(imagelist[i]) # Open the image.
        width, height = im1.size  # Get the width and height of that image.
        ## TODO: add flag to disable auto-rotate (and set rotation left/right)
        if width > height:
            im2 = im1.transpose(Image.ROTATE_270) # If width > height, rotate the image.
            os.remove(imagelist[i]) # Delete the previous image.
            im2.save(imagelist[i]) # Save the rotated image.
        # im.save

    print("\nFound " + str(len(imagelist)) + " image files. Converting to PDF....\n")

    # -------------- CONVERT TO PDF ------------ #

    for image in imagelist:
        pdf.add_page()
        pdf.image(image, 0, 0, 210, 297)  # 210 and 297 are the dimensions of an A4 size sheet.

    pdf.output(folder + "/" + name + ".pdf",
               "F")  # TODO: convert to path join # Save the PDF.

    print(
        "PDF generated successfully!\nAnd saved as " + folder + "/" + name + ".pdf") # TODO move to format and variables


if __name__ == "__main__":
    main(sys.argv[1:])
