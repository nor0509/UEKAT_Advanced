# import os
#
# from detector import detect_objects
#
# current_test_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.dirname(current_test_dir)
# img_path = os.path.join(project_root, "test_photo", "people.png")
# output_path = os.path.join(project_root, "results", "people-result.png")
# os.makedirs(os.path.dirname(output_path), exist_ok=True)
# print(detect_objects(img_path,output_path))