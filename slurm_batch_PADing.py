import random

import yaml
import subprocess


def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def save_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.safe_dump(data, file, sort_keys=False)


def update_yaml(base_yaml, set_dict):
    for key, value in set_dict.items():
        parts = key.split(".")
        current_dict = base_yaml
        for part in parts[:-1]:  # Traverse to the second last element
            current_dict = current_dict[part]
        current_dict[parts[-1]] = value  # Update the last element


# def generate_train_script(base_script, new_yaml_file, new_seed):
#     new_script = base_script.replace("SemGraphPAD.yaml", new_yaml_file)
#     new_script = new_script.replace("MSE_46617688", f"MSE_{new_seed}")
#     return new_script


def write_script_to_file(script_content, file_name):
    with open(file_name, 'w') as file:
        file.write(script_content)


def generate_random_number(s: int):
    if s == -1:
        num_digits = random.randint(5, 9)
        lower_bound = 10 ** (num_digits - 1)
        upper_bound = 10 ** num_digits - 1
        return random.randint(lower_bound, upper_bound)
    else:
        return s


if __name__ == '__main__':
    # generate seed or fix seed
    SEED = generate_random_number(-1)
    # # other params
    # LOSS_TYPE = "GMMN"
    # NOISE = False
    # WO_SEEN = False
    # WO_MASK_SCORES = False
    # WO_MASK_LABEL = False
    # # WO_EIGEN = True
    # # EIGEN_TYPE = "norm"
    # FT = True
    # FT_WEIGHT = True
    # NUM_CHOOSE = 14

    # run params
    gpu_num = 1
    gpu_type = "v100"
    gpu = f"{gpu_type}:{str(gpu_num)}"

    # exp id
    # exp_id = \
    #     f"{SEED}_{LOSS_TYPE}_{gpu_type}{'_eigen_' + EIGEN_TYPE if not WO_EIGEN else ''}{'_FT' if FT else ''}"
    exp_id = f"{SEED}"
        # f"{SEED}_{LOSS_TYPE}_{gpu_type}{'_FT' if FT else ''}"
    # if FT_WEIGHT:
    #     exp_id += "_WEIGHT"
    # if NUM_CHOOSE != 5:
    #     exp_id += f'_num{NUM_CHOOSE}'

    output_dir = f"res/{exp_id}"
    # set params
    set_dict = {
        "OUTPUT_DIR": output_dir,
        "SEED": SEED,
        # "SemGraphPADing.LOSS_TYPE": LOSS_TYPE,
        # "SemGraphPADing.NOISE": NOISE,
        # "SemGraphPADing.WO_SEEN": WO_SEEN,
        # "SemGraphPADing.WO_MASK_SCORES": WO_MASK_SCORES,
        # "SemGraphPADing.WO_MASK_LABEL": WO_MASK_LABEL,
        # # "SemGraphPADing.WO_EIGEN": WO_EIGEN,
        # # "SemGraphPADing.EIGEN_TYPE": EIGEN_TYPE
        # "SemGraphPADing.FT": FT,
        # "SemGraphPADing.FT_WEIGHT": FT_WEIGHT,
        # "MODEL.MASK_FORMER.NUM_CHOOSE": NUM_CHOOSE
    }

    # wandb_proj = "SemGraphPAD_v1.1"
    slurm_dir = f"slurmout/{exp_id}"
    new_yaml_file = f"PADing_{exp_id}.yaml"

    base_yaml = load_yaml('configs/panoptic-segmentation/PADing.yaml')
    update_yaml(base_yaml, set_dict)
    save_yaml(base_yaml, f'configs/panoptic-segmentation/{new_yaml_file}')
    print(f"use seed[{SEED}], yaml file now save in configs/panoptic-segmentation/{new_yaml_file}")

    # slurm script
    script_content = f"""#!/bin/sh
. ~/.bashrc
source activate
conda activate pading
CUDA_VISIBLE_DEVICES=0 python train_net.py  \
--config-file configs/panoptic-segmentation/{new_yaml_file}  \
--num-gpus {gpu_num} \
MODEL.WEIGHTS pretrained_weight_panoptic.pth"""

    script_file_name = f"./train_{exp_id}.sh"
    write_script_to_file(script_content, script_file_name)
    print(f"train script save in {script_file_name}")

    command = f"sbatch -N 1 -p zjhu -t 7-00:00:00 --cpus-per-task=8 --gres=gpu:{gpu} -o {slurm_dir} {script_file_name}"
    subprocess.run(command, shell=True)
    print("submit completion!")
