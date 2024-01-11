import os
import xmltodict


def convert_xml_annotation_to_yolo_txt_annotation(xml_annotation_dir, yolo_txt_dir, class_mapping):
    for filename in os.listdir(path=xml_annotation_dir):
        if filename.endswith(".xml"):
            with open(file=os.path.join(xml_annotation_dir, filename), mode='r') as file:
                data = xmltodict.parse(xml_input=file.read())

            img_width = int(data['annotation']['size']['width'])
            img_height = int(data['annotation']['size']['height'])

            # print(img_width, img_height)

            yolo_txt_path = os.path.join(yolo_txt_dir, filename.replace(".xml", ".txt"))

            with open(file=yolo_txt_path, mode='w') as file:
                objects = data['annotation']['object']
                if not isinstance(objects, list):
                    objects = [objects]  # Convert to list if it's not already
                for obj in objects:
                    class_name = obj['name']
                    # print(class_name)
                    class_id = class_mapping.get(class_name)
                    if class_id is not None:
                        x_min = int(obj['bndbox']['xmin']) # Based on xml file format you have to change this code
                        y_min = int(obj['bndbox']['ymin'])
                        x_max = int(obj['bndbox']['xmax'])
                        y_max = int(obj['bndbox']['ymax'])
                        x_center = (x_min + x_max) / 2 / img_width
                        y_center = (y_min + y_max) / 2 / img_height
                        width = (x_max - x_min) / img_width
                        height = (y_max - y_min) / img_height

                        file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

if __name__ == '__main__':
    # Example usage
    class_mapping = {
        'hyperplastic': 0,
        'adenomatous': 1,
    }

    xml_annotation_dir = r'seperate\New folder\Final Data\train\labels'
    yolo_txt_dir = r'seperate\New folder\Final Data\train\labels2' # all file will be save this location

    convert_xml_annotation_to_yolo_txt_annotation(xml_annotation_dir, yolo_txt_dir, class_mapping)
    print("Completed conversion")