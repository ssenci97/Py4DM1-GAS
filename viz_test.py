from semmeta import SEMVisualizer

img_path = 'imgs/1/12_50_vero_09.tif'
json_path = 'mock/json-clean.json'
test = SEMVisualizer(json_path, img_path)
test.show_image_with_table()
