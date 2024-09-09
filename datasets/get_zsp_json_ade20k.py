import json
import argparse


def filter_annotation_unseen(anno_dict, split_name_list, class_id_to_split):
    filtered_images = []
    filtered_annotations = []
    useful_image_ids = set()
    # 把unseen的图片信息加入到filtered_annotations中
    for item in anno_dict['annotations']:
        for segment in item['segments_info']:
            if class_id_to_split.get(segment['category_id']) in split_name_list:
                filtered_annotations.append(item)
                useful_image_ids.add(item['image_id'])
                break

    for item in anno_dict['images']:
        if item['id'] in useful_image_ids:
            filtered_images.append(item)
    anno_dict['annotations'] = filtered_annotations
    anno_dict['images'] = filtered_images


def filter_annotation_seen(anno_dict, split_name_list, class_id_to_split):
    filtered_images = []
    filtered_annotations = []
    useful_image_ids = set()
    # 把仅包含seen的放在filtered_annotations里
    for item in anno_dict['annotations']:
        unseen = False
        for segment in item['segments_info']:
            if class_id_to_split.get(segment['category_id']) in ['unseen']:
                unseen = True
        if not unseen:
            filtered_annotations.append(item)
            useful_image_ids.add(item['image_id'])
    # 仅包含see的图片
    for item in anno_dict['images']:
        if item['id'] in useful_image_ids:
            filtered_images.append(item)
    anno_dict['annotations'] = filtered_annotations
    anno_dict['images'] = filtered_images


def change_all_annotations(anno_dict, class_id_to_split):
    filtered_categories = []
    for item in anno_dict['categories']:
        item['split'] = class_id_to_split.get(item['id'])
        filtered_categories.append(item)
    anno_dict['categories'] = filtered_categories


def convert_json(save_dir, annotation_dir):
    with open(annotation_dir + 'ade20k_panoptic_train.json', 'r') as fin:
        ade20k_train_anno_all = json.load(fin)
    with open(annotation_dir + 'ade20k_panoptic_train.json', 'r') as fin:
        ade20k_train_anno_seen = json.load(fin)
    with open(annotation_dir + 'ade20k_panoptic_train.json', 'r') as fin:
        ade20k_train_anno_unseen = json.load(fin)
    with open(annotation_dir + 'ade20k_panoptic_val.json', 'r') as fin:
        ade20k_val_anno_all = json.load(fin)
    with open(annotation_dir + 'ade20k_panoptic_val.json', 'r') as fin:
        ade20k_val_anno_seen = json.load(fin)
    with open(annotation_dir + 'ade20k_panoptic_val.json', 'r') as fin:
        ade20k_val_anno_unseen = json.load(fin)
    with open('datasets/ade20k_unseen_classes.json', 'r') as fin:
        labels_unseen = json.load(fin)

    print('Loading successfully')

    class_id_to_split = {}
    class_name_to_split = {}
    for item in ade20k_val_anno_all['categories']:
        if item['name'] not in labels_unseen:
            class_id_to_split[item['id']] = 'seen'
            class_name_to_split[item['name']] = 'seen'
        else:
            class_id_to_split[item['id']] = 'unseen'
            class_name_to_split[item['name']] = 'unseen'

    change_all_annotations(ade20k_train_anno_all, class_id_to_split)
    change_all_annotations(ade20k_val_anno_all, class_id_to_split)
    filter_annotation_seen(ade20k_train_anno_seen, ['seen'], class_id_to_split)
    filter_annotation_unseen(ade20k_train_anno_unseen, ['unseen'], class_id_to_split)
    filter_annotation_seen(ade20k_val_anno_seen, ['seen'], class_id_to_split)
    filter_annotation_unseen(ade20k_val_anno_unseen, ['unseen'], class_id_to_split)

    print(len(ade20k_val_anno_seen['categories']), len(ade20k_val_anno_unseen['categories']), len(ade20k_train_anno_seen['categories']), len(ade20k_train_anno_unseen['categories']))
    print(len(ade20k_val_anno_seen['images']), len(ade20k_val_anno_unseen['images']), len(ade20k_train_anno_seen['images']), len(ade20k_train_anno_unseen['images']))
    # import pdb; pdb.set_trace()
    with open(save_dir + 'panoptic_train_seen.json', 'w') as fout:
        json.dump(ade20k_train_anno_seen, fout)
    with open(save_dir + 'panoptic_train_unseen.json', 'w') as fout:
        json.dump(ade20k_train_anno_unseen, fout)
    with open(save_dir + 'panoptic_train_all.json', 'w') as fout:
        json.dump(ade20k_train_anno_all, fout)
    with open(save_dir + 'panoptic_val_seen.json', 'w') as fout:
        json.dump(ade20k_val_anno_seen, fout)
    with open(save_dir + 'panoptic_val_unseen.json', 'w') as fout:
        json.dump(ade20k_val_anno_unseen, fout)
    with open(save_dir + 'panoptic_val_all.json', 'w') as fout:
        json.dump(ade20k_val_anno_all, fout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save_dir", type=str, default="datasets/ADEChallengeData2016/annotations/ZSP/")
    parser.add_argument("--annotation_dir", type=str, default="datasets/ADEChallengeData2016/")
    args = parser.parse_args()
    convert_json(args.save_dir, args.annotation_dir)


if __name__ == "__main__":
    main()