#!/bin/bash

# Pretrained
LINK_PRETRAIN=1
PRETRAIN_INSTANCE="./pretrained_weight_instance.pth"
PRETRAIN_PANOPTIC="./pretrained_weight_panoptic.pth"
PRETRAIN_SEMANTIC="./pretrained_weight_semantic.pth"
if [ "$LINK_PRETRAIN" -eq 1 ]; then
    if [ ! -L "$PRETRAIN_INSTANCE" ]; then
        ln -s "/home/pengwei/datasets/pretrain_model/PADing/pretrained_weight_instance.pth" "$PRETRAIN_INSTANCE"
        echo "Soft link created for INSTANCE pretrained model"
    else
        echo "Soft link of INSTANCE pretrained model already exists. No action taken."
    fi
    if [ ! -L "$PRETRAIN_PANOPTIC" ]; then
        ln -s "/home/pengwei/datasets/pretrain_model/PADing/pretrained_weight_panoptic.pth" "$PRETRAIN_PANOPTIC"
        echo "Soft link created for PANOPTIC pretrained model"
    else
        echo "Soft link of PANOPTIC pretrained model already exists. No action taken."
    fi
    if [ ! -L "$PRETRAIN_SEMANTIC" ]; then
        ln -s "/home/pengwei/datasets/pretrain_model/PADing/pretrained_weight_semantic.pth" "$PRETRAIN_SEMANTIC"
        echo "Soft link created for SEMANTIC pretrained model"
    else
        echo "Soft link of SEMANTIC pretrained model already exists. No action taken."
    fi
else
    echo "Skipping link creation for pretrained model"
fi



# COCO2014
LINK_COCO2014=1
COCO2014_TR_PATH="datasets/coco/train2014"
COCO2014_VA_PATH="datasets/coco/val2014"

# COCO2017
LINK_COCO2017=1
COCO2017_TR_PATH="datasets/coco/train2017"
COCO2017_VA_PATH="datasets/coco/val2017"

# COCO2017_panoptic
LINK_COCO2017_panoptic=1
COCO2017_panoptic_TR_PATH="datasets/coco/panoptic_train2017"
COCO2017_panoptic_VA_PATH="datasets/coco/panoptic_val2017"

# COCO2017_panoptic_semseg (generated)
LINK_COCO2017_panoptic_semseg=1
COCO2017_panoptic_semseg_TR_PATH="datasets/coco/panoptic_semseg_train2017"
COCO2017_panoptic_semseg_VA_PATH="datasets/coco/panoptic_semseg_val2017"
# Annotations
LINK_ANNOTATION=1
ANNOTATION_PATH="datasets/coco/annotations"
# Coco_STUFF
LINK_COCO_STUFF=1
COCO_STUFF_PATH="datasets/coco/coco_stuff"

# Function to create soft links with directory checks
link_dataset() {
    local dataset_path=$1
    local target_link_path=$2
    local link_control=$3

    # Check if the parent directory of the target link path exists
    local parent_dir=$(dirname "$target_link_path")
    if [ ! -d "$parent_dir" ]; then
        echo "Parent directory $parent_dir does not exist. Creating it now..."
        mkdir -p "$parent_dir"
    fi

    # Check if soft link already exists and if control is 1
    if [ "$link_control" -eq 1 ]; then
        if [ ! -L "$target_link_path" ]; then
            ln -s "$dataset_path" "$target_link_path"
            echo "Soft link created for $dataset_path at $target_link_path"
        else
            echo "Soft link $target_link_path already exists. No action taken."
        fi
    else
        echo "Skipping link creation for $dataset_path"
    fi
}

link_dataset "/home/pengwei/datasets/coco/train2014" "$COCO2014_TR_PATH" $LINK_COCO2014
link_dataset "/home/pengwei/datasets/coco/val2014" "$COCO2014_VA_PATH" $LINK_COCO2014

link_dataset "/home/pengwei/datasets/coco/train2017" "$COCO2017_TR_PATH" $LINK_COCO2017
link_dataset "/home/pengwei/datasets/coco/val2017" "$COCO2017_VA_PATH" $LINK_COCO2017

link_dataset "/home/pengwei/datasets/coco/panoptic_train2017" "$COCO2017_panoptic_TR_PATH" $LINK_COCO2017_panoptic
link_dataset "/home/pengwei/datasets/coco/panoptic_val2017" "$COCO2017_panoptic_VA_PATH" $LINK_COCO2017_panoptic

link_dataset "/home/pengwei/datasets/coco/panoptic_semseg_train2017" "$COCO2017_panoptic_semseg_TR_PATH" $LINK_COCO2017_panoptic_semseg
link_dataset "/home/pengwei/datasets/coco/panoptic_semseg_val2017" "$COCO2017_panoptic_semseg_VA_PATH" $LINK_COCO2017_panoptic_semseg

link_dataset "/home/pengwei/datasets/coco/annotations" "$ANNOTATION_PATH" $LINK_ANNOTATION
link_dataset "/home/pengwei/datasets/coco/coco_stuff" "$COCO_STUFF_PATH" $LINK_COCO_STUFF

