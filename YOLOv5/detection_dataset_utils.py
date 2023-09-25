"""
This is a utility file designed for preprocessing data in a detection dataset.

This file serves the purpose of performing necessary data preparation tasks prior to training a model.

Within this file, you'll find the following functions:

1. Remove Unnecessary Object Annotations:
    This function checks the Pascal VOC format annotation file and removes object annotations that are no longer required.

2. Delete Blank Annotation Files:
    Here, we identify and delete annotation files that lack object annotations. In other words, these are annotation files with no specified objects.

3. Remove Unlinked Annotation Files:
    Annotations that have no corresponding image files are deleted by this function.

4. Remove Unlinked Image Files:
    This function ensures that image files without corresponding annotations are removed.

5. Extract Class Names:
    You can use this function to extract all class names present in the Pascal VOC format annotation file.

6. Correct Spelling Mistakes:
    In cases of misspelled annotation tag names, this function can help you correct them.

7. Remove Out-of-Image Annotations:
    The annotation box coordinates are checked and annotations falling outside the image boundaries are removed.

8. Adjust Annotation Box Dimensions:
    This function verifies and corrects annotation box dimensions that do not match the image's actual width and height.

9. Convert to YOLO Format:
    Transform your annotations from Pascal VOC format to YOLO format using this function.

10. Convert to Pascal VOC Format:
    Conversely, this function allows you to convert annotations from YOLO format back to Pascal VOC format.

11. Dataset Splitting:
    Lastly, you can employ this function to divide your dataset into training, validation, and testing segments.

The aim of these functions is to streamline your data and annotations, making them more suitable for efficient model training.
"""

import random
import shutil
from os import PathLike
from pathlib import Path

from typing import Union, List, Tuple, Dict, NoReturn

import xml.etree.ElementTree as ET

import logging

from tqdm import tqdm

logging.basicConfig(level=logging.INFO)


class DetectionDataUtils(object):
    def __init__(self, image_dir: Union[str, Path, PathLike], annotation_dir: Union[str, Path, PathLike]):
        """
        初始化,传入图片目录和标注目录
        :param image_dir: the directory of the images, it can be a string, Path or PathLike object
        :param annotation_dir: the directory of the annotations, it can be a string, Path or PathLike object
        """

        assert Path(image_dir).exists(), f'图片目录{image_dir}不存在'
        assert Path(annotation_dir).exists(), f'标注目录{annotation_dir}不存在'
        # convert the image_dir and annotation_dir to Path object
        if not isinstance(image_dir, Path):
            image_dir = Path(image_dir)
        if not isinstance(annotation_dir, Path):
            annotation_dir = Path(annotation_dir)
        self.image_dir = image_dir
        self.annotation_dir = annotation_dir
        self.yolo_annotation_dir = None
        self.classes = []
        self.image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg']
        self.logger = logging.getLogger(__name__)

    def show_data_status(self) -> None:
        """
        查看数据集的状态，包括图片数量和标注文件数量
        :return: None
        """
        image_files = [file for file in self.image_dir.glob('*') if file.suffix.lower() in self.image_extensions]

        label_files = list(self.annotation_dir.glob('*.xml'))
        self.logger.info(f'数据集共有{len(image_files)}张图片，{len(label_files)}个标注文件')

    def extract_class_names(self) -> List[str]:
        """
        查看数据集中的所有类别名称
        :return: a list of class names
        """
        self.classes = []
        annotation_files = list(self.annotation_dir.glob('*.xml'))
        self.logger.info("Start Extracting Class Names ...")
        for annotation_file in tqdm(annotation_files):
            tree = ET.parse(annotation_file)
            root = tree.getroot()
            objects = root.findall('object')
            for obj in objects:
                name = obj.find('name').text
                if name not in self.classes:
                    self.classes.append(name)
        self.logger.info(f'数据集共有{len(self.classes)}个类别，分别为{self.classes}')
        return self.classes

    def remove_objects(self, object_names: List[str], inplace: bool = True):
        """
        删除指定的标注数据,将xml文件中的object标签删除
        :param object_names:
        :param inplace:
        :return:
        """
        annotation_files = list(self.annotation_dir.glob('*.xml'))
        for annotation_file in annotation_files:
            tree = ET.parse(annotation_file)
            root = tree.getroot()
            objects = root.findall('object')
            for obj in objects:
                name = obj.find('name').text
                if name in object_names:
                    root.remove(obj)
                    self.logger.info(f'{annotation_file.name}已删除{object_names}标注')
            if inplace:
                tree.write(annotation_file)
        self.logger.info(f"===标注文件{object_names}删除完成===")

    def remove_blank_annotation_files(self):
        """
        删除空的标注文件
        :return: None
        """
        annotation_files = list(self.annotation_dir.glob('*.xml'))
        self.logger.info("Start Scanning Blank Annotation Files ...")
        for annotation_file in tqdm(annotation_files):
            tree = ET.parse(annotation_file)
            root = tree.getroot()
            objects = root.findall('object')
            if len(objects) == 0:
                self.logger.info(f'空标注文件<<{annotation_file.name}>>已删除')
                annotation_file.unlink()
        self.logger.info(f'===空标注文件删除完成===')

    def remove_redundant_files(self):
        """
        删除冗余的标注文件和图片文件，即标注文件和图片文件名称不匹配的文件
        :return: None
        """
        annotation_files = list(self.annotation_dir.glob('*.xml'))
        for annotation_file in annotation_files:
            # find the image file corresponding to the annotation file
            # image_file = self.image_dir / (annotation_file.stem + '.jpg')

            # assume that there is only one image file corresponding to the annotation file
            image_file = [self.image_dir / (annotation_file.stem + ext) for ext in self.image_extensions if
                          (self.image_dir / (annotation_file.stem + ext)).exists()][0]

            if not image_file.exists():
                self.logger.info(f'冗余标注文件<<{annotation_file.name}>>已删除')
                annotation_file.unlink()

        image_files = [file for file in self.image_dir.glob('*') if file.suffix.lower() in self.image_extensions]

        for image_file in image_files:
            # find the annotation file corresponding to the image file
            annotation_file = self.annotation_dir / (image_file.stem + '.xml')
            if not annotation_file.exists():
                self.logger.info(f'冗余图片文件<<{image_file.name}>>已删除')
                image_file.unlink()
        self.logger.info(f'===冗余图片与标注文件删除完成===')

    def correct_spelling_mistakes(self, corrigenda: Dict[str, str], inplace: bool = True):
        """
        校正标注文件中的拼写错误
        :param corrigenda:  勘误表，字典格式，key为错误的拼写，value为正确的拼写, 例如{'peoson':'person'}
        :param inplace:
        :return:
        """
        assert isinstance(corrigenda, dict), 'corrigenda必须是字典'
        assert len(self.classes) > 0, '请先提取类别名称'
        incorrect_spellings = list(corrigenda.keys())
        annotation_files = list(self.annotation_dir.glob('*.xml'))
        self.logger.info("Start Correcting Spelling Mistakes ...")
        for annotation_file in tqdm(annotation_files):
            tree = ET.parse(annotation_file)
            root = tree.getroot()
            objects = root.findall('object')
            for obj in objects:
                name = obj.find('name').text
                if name in incorrect_spellings:
                    correct_spelling = corrigenda[name]
                    obj.find('name').text = correct_spelling
                    self.logger.info(f"标注文件<<{annotation_file.name}>>已修正 {name} --> {correct_spelling}")
                    self.logger.info(f'标注文件<<{annotation_file.name}>>修正完成')
            if inplace:
                tree.write(annotation_file)
        self.logger.info(f'===标注文件拼写错误修正完成===')
        self.logger.info(f'===更新数据集类别列表===')
        self.classes = self.extract_class_names()

    def validate_out_of_image_annotations(self) -> None:
        annotation_files = list(self.annotation_dir.glob('*.xml'))
        unqualified_annotation_files = []
        for annotation_file in tqdm(annotation_files):
            tree = ET.parse(annotation_file)
            root = tree.getroot()
            objects = root.findall('object')
            # get the image size
            size = root.find('size')
            width = int(size.find('width').text)
            height = int(size.find('height').text)

            for obj in objects:
                bndbox = obj.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)
                if xmin < 0 or ymin < 0 or xmax > width or ymax > height:
                    # self.logger.info(f'标注文件<<{annotation_file.name}>>存在超出图片范围的标注')
                    if annotation_file not in unqualified_annotation_files:
                        unqualified_annotation_files.append(annotation_file)
        if len(unqualified_annotation_files) > 0:
            self.logger.info(f'存在超出图片范围的标注文件，共{len(unqualified_annotation_files)}个')
            # for file in unqualified_annotation_files:
            #     self.logger.info(file.name)
        else:
            self.logger.info(f'不存在超出图片范围的标注文件')

    def modify_out_of_image_annotations(self, inplace: bool = True) -> None:
        """
        修改标注文件中的标注框超出图片范围的标注
        :return: None
        """
        annotation_files = list(self.annotation_dir.glob('*.xml'))
        for annotation_file in annotation_files:
            tree = ET.parse(annotation_file)
            root = tree.getroot()
            objects = root.findall('object')
            # get the image size
            size = root.find('size')
            width = int(size.find('width').text)
            height = int(size.find('height').text)

            for obj in objects:
                bndbox = obj.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)
                if xmin < 0:
                    bndbox.find('xmin').text = '0'
                    self.logger.info(f'标注文件<<{annotation_file.name}>>已修正 xmin')
                if ymin < 0:
                    bndbox.find('ymin').text = '0'
                    self.logger.info(f'标注文件<<{annotation_file.name}>>已修正 ymin')
                if xmax > width:
                    bndbox.find('xmax').text = str(width)
                    self.logger.info(f'标注文件<<{annotation_file.name}>>已修正 xmax')
                if ymax > height:
                    bndbox.find('ymax').text = str(height)
                    self.logger.info(f'标注文件<<{annotation_file.name}>>已修正 ymax')
            if inplace:
                tree.write(annotation_file)
        self.logger.info(f'===标注文件超出图片范围的标注修正完成===')

    def remove_out_of_image_annotations(self, inplace: bool = True) -> None:
        """
        移除标注超出图片范围的标注
        :return: None
        """
        annotation_files = list(self.annotation_dir.glob('*.xml'))
        for annotation_file in annotation_files:
            tree = ET.parse(annotation_file)
            root = tree.getroot()
            objects = root.findall('object')
            # get the image size
            size = root.find('size')
            width = int(size.find('width').text)
            height = int(size.find('height').text)

            for obj in objects:
                bndbox = obj.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)
                if xmin < 0 or ymin < 0 or xmax > width or ymax > height:
                    root.remove(obj)
                    self.logger.info(f'标注文件<<{annotation_file.name}>>已删除超出图片范围的标注')
            if inplace:
                tree.write(annotation_file)
        self.logger.info(f'===标注文件超出图片范围的标注项删除完成===')

    def adjust_annotation_box_dimensions(self, inplace: bool = True) -> None:
        """
        修改标注文件中的标注框与实际图片不匹配的宽度和高度数据
        :return: None
        """
        pass

    @staticmethod
    def xyxy2xywh(size: Tuple[int, int], box: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
        """
        将(xmin,ymin,xmax,ymax)格式转换为(x,y,w,h)格式
        Args:
            size(tuple[int,int]): 图像的宽与高
            box(tuple[float,float,float,float]):

        Returns:
            tuple[float, float, float, float],返回XYWH格式的标注框数据,数值均归一化到[0,1]

        """
        dw = 1. / size[0]
        dh = 1. / size[1]
        x = (box[0] + box[2]) / 2 * dw
        y = (box[1] + box[3]) / 2 * dh
        w = (box[2] - box[0]) * dw
        h = (box[3] - box[1]) * dh
        return x, y, w, h

    def convert_to_yolo_format(self, dst_anno_dir: Union[str, Path] = 'labels_tmp') -> NoReturn:
        """
        将标注文件转换为yolo格式
        :param dst_anno_dir: 保存yolo格式标注文件的目录
        :return:
        """
        # create a directory to store the yolo format annotation files which is named as 'labels' by default
        # this directory is created with the same parent directory as the annotation directory

        if not isinstance(dst_anno_dir, Path):
            dst_anno_dir = self.annotation_dir.parent / dst_anno_dir
        dst_anno_dir.mkdir(parents=True, exist_ok=True)
        self.yolo_annotation_dir = dst_anno_dir
        # get all the annotation files
        annotation_files = list(self.annotation_dir.glob('*.xml'))
        if self.classes is None or len(self.classes) == 0:
            self.logger.info("Start Extracting Class Names ...")
            self.extract_class_names()
        # write all the class names into classes.txt
        with open(dst_anno_dir.parent / 'classes.txt', 'w+', encoding='utf-8') as fw:
            fw.write("\n".join(self.classes))

        self.logger.info("Start Processing Annotation files' format from Pascal VOC to YOLO ...")
        for file in tqdm(annotation_files):
            annotation_text_filename = file.name.replace('xml', 'txt')
            out_file = open(dst_anno_dir / annotation_text_filename, 'w', encoding='utf-8')
            # 开始解析xml文件
            tree = ET.parse(file)
            root = tree.getroot()
            # 图片的shape值
            size = root.find('size')
            w = int(size.find('width').text)
            h = int(size.find('height').text)
            #
            for obj in root.iter('object'):
                difficult = obj.find('difficult').text
                cls = obj.find('name').text
                if cls not in self.classes or int(difficult) == 1:
                    continue
                # 将名称转换为id下标
                cls_id = self.classes.index(cls)
                # 获取整个bounding box框
                bndbox = obj.find('bndbox')
                # xml给出的是x1, y1, x2, y2
                box = (
                    float(bndbox.find('xmin').text),
                    float(bndbox.find('ymin').text),
                    float(bndbox.find('xmax').text),
                    float(bndbox.find('ymax').text)
                )
                #
                # 将x1, y1, x2, y2转换成yolov5所需要的x_center, y_center, w, h格式
                bbox = self.xyxy2xywh((w, h), box)
                # 写入目标文件中，格式为 id x y w h
                out_file.write(str(cls_id) + " " + " ".join(str(x) for x in bbox) + '\n')
        self.logger.info("===标注文件格式转换完成===")

    def split_dataset_train_val(self, root_dir: str = "data", train_ratio: float = 0.8, val_ratio: float = 0.1, ):
        """
        拆分图片与YOLO格式标注文件为训练集、验证集和测试集，默认比例为8:1:1
        :param root_dir: YOLO格式标注文件目录
        :param train_ratio: 训练集比例
        :param val_ratio: 验证集比例
        :return:
        """
        # the train,val and test are separated by 8:1:1, each part contains images and labels directory
        root_dir = self.image_dir.parent / root_dir
        images_dir = Path(root_dir) / 'images'
        label_dir = Path(root_dir) / 'labels'

        train_image_dir = images_dir / 'train'
        train_label_dir = label_dir / 'train'

        val_image_dir = images_dir / 'val'
        val_label_dir = label_dir / 'val'

        test_image_dir = images_dir / 'test'
        test_label_dir = label_dir / 'test'

        train_image_dir.mkdir(parents=True, exist_ok=True)
        train_label_dir.mkdir(parents=True, exist_ok=True)

        val_image_dir.mkdir(parents=True, exist_ok=True)
        val_label_dir.mkdir(parents=True, exist_ok=True)

        test_image_dir.mkdir(parents=True, exist_ok=True)
        test_label_dir.mkdir(parents=True, exist_ok=True)

        image_files = [file for file in self.image_dir.glob('*') if file.suffix.lower() in self.image_extensions]
        label_files = list(self.yolo_annotation_dir.glob('*.txt'))

        # shuffle the image files and label files while maintaining the correspondence between them
        random.seed(2021)
        random.shuffle(image_files)
        random.seed(2021)
        random.shuffle(label_files)

        train_image_files = image_files[:int(len(image_files) * train_ratio)]
        train_label_files = label_files[:int(len(label_files) * train_ratio)]

        val_image_files = image_files[
                          int(len(image_files) * train_ratio):int(len(image_files) * (train_ratio + val_ratio))]
        val_label_files = label_files[
                          int(len(label_files) * train_ratio):int(len(label_files) * (train_ratio + val_ratio))]

        test_image_files = image_files[int(len(image_files) * (train_ratio + val_ratio)):]
        test_label_files = label_files[int(len(label_files) * (train_ratio + val_ratio)):]

        self.logger.info(f'训练集共有{len(train_image_files)}张图片，{len(train_label_files)}个标注文件')
        self.logger.info("Start Copying Train Dataset ...")
        for image_file, label_file in zip(train_image_files, train_label_files):
            shutil.copy(image_file, train_image_dir / image_file.name)
            shutil.copy(label_file, train_label_dir / label_file.name)

        with open(train_label_dir / 'classes.txt', 'w+', encoding='utf-8') as fw:
            fw.write('\n'.join(self.classes))

        self.logger.info(f'验证集共有{len(val_image_files)}张图片，{len(val_label_files)}个标注文件')
        self.logger.info("Start Copying Val Dataset ...")
        for image_file, label_file in zip(val_image_files, val_label_files):
            shutil.copy(image_file, val_image_dir / image_file.name)
            shutil.copy(label_file, val_label_dir / label_file.name)

        with open(val_label_dir / 'classes.txt', 'w+', encoding='utf-8') as fw:
            fw.write('\n'.join(self.classes))

        self.logger.info(f'测试集共有{len(test_image_files)}张图片，{len(test_label_files)}个标注文件')
        self.logger.info("Start Copying Test Dataset ...")
        for image_file, label_file in zip(test_image_files, test_label_files):
            shutil.copy(image_file, test_image_dir / image_file.name)
            shutil.copy(label_file, test_label_dir / label_file.name)

        with open(test_label_dir / 'classes.txt', 'w+', encoding='utf-8') as fw:
            fw.write('\n'.join(self.classes))
        self.logger.info("===数据集拆分完成===")


def main():
    # 1. 设置图片目录和标注目录
    image_dir = Path('test_data/JPEGImages')
    annotation_dir = Path('test_data/Annotations')
    # 2. 创建数据集工具类对象
    data_utils = DetectionDataUtils(image_dir, annotation_dir)
    # 查看数据集状态
    data_utils.show_data_status()

    # 3. (可选)移除指定的标注数据
    # data_utils.remove_objects(['car'])
    # 4. 移除空的标注文件
    data_utils.remove_blank_annotation_files()
    data_utils.show_data_status()
    # 5. 移除冗余的标注文件和图片文件
    data_utils.remove_redundant_files()
    data_utils.show_data_status()

    # 查看数据集中的所有类别名称
    print(data_utils.extract_class_names())
    # 6. (可选)校正标注文件中的拼写错误
    # corrigenda = {'seal003': "seal", 'seal000': 'seal'}
    # data_utils.correct_spelling_mistakes(corrigenda)

    # 7. 移除标注超出图片范围的标注
    data_utils.remove_out_of_image_annotations()
    # 8. 转换数据格式为YOLO格式
    data_utils.convert_to_yolo_format()
    # 9. 拆分数据集为训练集、验证集和测试集
    data_utils.split_dataset_train_val()


if __name__ == '__main__':
    """
    脚本使用方法：
    按照main方法中的步骤执行即可，非必选项需要执行可放开注释，修改参数后执行即可
    执行前建议备份数据集，脚本中的相关读写与删除操作都是原地执行，是不可逆的
    执行脚本前的数据集目录结构如下：
    ├── Annotations
    │      ├── 000000.xml
    │      ├── 000001.xml
    ├── JPEGImages
    │      ├── 000000.jpg
    │      ├── 000001.jpg
    
    执行脚本后的数据集目录结构如下：
    ├── Annotations
    ├── JPEGImages
    ├── labels
    ├── data
    │      ├── train
    │      │      ├── images
    │      │      ├── labels
    │      │      │      ├── classes.txt
    │      ├── val
    │      │      ├── images
    │      │      ├── labels
    │      │      │      ├── classes.txt
    │      ├── test
    │      │      ├── images
    │      │      ├── labels
    │      │      │      ├── classes.txt
    
    data目录下的train,val,test目录分别包含images和labels两个子目录，images目录存放图片文件，labels目录存放标注文件
    labels目录下的classes.txt文件存放数据集中的类别名称
    YOLO配置文件按照对应的路径和类别名称进行修改即可。    
    """

    # main()

    # 1. 设置图片目录和标注目录
    image_dir = Path(r"data/images")
    annotation_dir = Path(r"data/annotations")
    # 2. 创建数据集工具类对象
    data_utils = DetectionDataUtils(image_dir, annotation_dir)
    # 查看数据集状态
    data_utils.show_data_status()

    exit(0)
