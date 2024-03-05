

def reduce_size(image_bin, ratio):
    import numpy as np
    from PIL import Image
    from io import BytesIO
    # Load your image
    img = Image.open(BytesIO(image_bin))
    img_array = np.array(img)
    new_size = tuple(map(lambda x: x // ratio, img.size))
    mid = ratio//2 - 1

    # Initialize an empty array for the reduced image
    reduced_img_array = np.empty((new_size[0], new_size[1], 3), dtype=np.uint8)  # Assuming a 3-channel RGB image

    # Loop over every 2x2 block and take the upper-left pixel
    for i in range(0, img.size[0], ratio):
        for j in range(0, img.size[1], ratio):
            reduced_img_array[i//ratio, j//ratio] = img_array[i + mid, j + mid]

    # Convert the reduced array back to an image
    reduced_img = Image.fromarray(reduced_img_array)

    with BytesIO() as img_bytes:
        # Save the image to the BytesIO object, specifying the format if necessary
        reduced_img.save(img_bytes, format='PNG')  # You can change 'PNG' to your desired format
        
        return img_bytes.getvalue()


def enlarge_size(image_bin, ratio):
    import numpy as np
    from PIL import Image
    from io import BytesIO
    # Load your image
    img = Image.open(BytesIO(image_bin))
    img_array = np.array(img)
    new_size = tuple(map(lambda x: x * ratio, img.size))

    enlarged_img_array = np.empty((new_size[0], new_size[1], 3), dtype=np.uint8)  # Assuming a 3-channel RGB image

    for i in range(0, img.size[0]):
        for j in range(0, img.size[1]):
            for k in range(0, ratio):
                for l in range(0, ratio):
                    enlarged_img_array[i*ratio+k, j*ratio+l] = img_array[i, j]

    enlarged_img = Image.fromarray(enlarged_img_array)

    with BytesIO() as img_bytes:
        # Save the image to the BytesIO object, specifying the format if necessary
        enlarged_img.save(img_bytes, format='PNG')  # You can change 'PNG' to your desired format
        
        return img_bytes.getvalue()
