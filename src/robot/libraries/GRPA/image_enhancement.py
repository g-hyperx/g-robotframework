from PIL import Image

def _resize_image(input_img_path=None, output_img_path=None, width=None, height=None):
    try:
        image = Image.open(input_img_path)
        new_size = (int(width), int(height))
        resized_image = image.resize(new_size)
        resized_image.save(output_img_path)
        return "Success"
    except Exception as ex:
        return ex
    
def _get_image_size(input_img_path=None):
    image = Image.open(input_img_path)
    width, height = image.size
    output_size = {"width":width,"height":height}
    return output_size