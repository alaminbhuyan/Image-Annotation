import os
import cv2


input_dir = r'combined dataset (d1d2d3)\masks'
output_dir = r'combined dataset (d1d2d3)\labels'

try:
    for j in os.listdir(path=input_dir):
        image_path = os.path.join(input_dir, j)
        # load the binary mask and get its contours
        mask = cv2.imread(filename=image_path, flags=cv2.IMREAD_GRAYSCALE)
        # cv2.threshold(src: MatLike,thresh: float,maxval: float,type: int,dst: MatLike | None)
        _, mask = cv2.threshold(src=mask, thresh=1, maxval=255, type=cv2.THRESH_BINARY)

        H, W = mask.shape # height, width
        # cv2.findContours(
        # image: MatLike,
        # mode: int,
        # method: int,
        # contours: Sequence[MatLike] | None = ...,
        # hierarchy: MatLike | None = ...,
        # offset: Point = ...
        # )
        contours, hierarchy = cv2.findContours(image=mask, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

        # convert the contours to polygons
        polygons = []
        for contour in contours:
            if cv2.contourArea(contour) > 200:
                polygon = []
                for point in contour:
                    x, y = point[0]
                    polygon.append(x / W)
                    polygon.append(y / H)
                polygons.append(polygon)

        # print the polygons
        with open(file='{}.txt'.format(os.path.join(output_dir, j)[:-4]), mode='w') as f:
            for polygon in polygons:
                for p_, p in enumerate(polygon):
                    if p_ == len(polygon) - 1:
                        f.write('{}\n'.format(p))
                    elif p_ == 0:
                        f.write('0 {} '.format(p))
                    else:
                        f.write('{} '.format(p))

            f.close()
except Exception as e:
    print(f"Error: {e}")
finally:
    print("Operation Done")