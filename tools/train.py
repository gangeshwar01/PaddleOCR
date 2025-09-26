# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, '..')))

import yaml
import paddle
import paddle.distributed as dist
from ppocr.data import build_dataloader
from ppocr.modeling.architectures import build_model
from ppocr.losses import build_loss
from ppocr.optimizer import build_optimizer
from ppocr.postprocess import build_post_process
from ppocr.metrics import build_metric
from ppocr.utils.save_load import load_model
from ppocr.utils.utility import set_seed
from ppocr.engine import Engine
from ppocr.utils.logging import get_logger
from ppocr.utils.config import get_config


def main(config, device, logger, vdl_writer):
    # init dist environment
    if config['Global']['distributed']:
        dist.init_parallel_env()

    # set seed
    seed = config['Global'].get('seed', 2022)
    set_seed(seed)

    # create dataloader
    train_dataloader = build_dataloader(config, 'Train', device, logger,
                                        seed)
    if config['Eval']:
        valid_dataloader = build_dataloader(config, 'Eval', device, logger,
                                            seed)
    else:
        valid_dataloader = None

    # build post process
    post_process_class = build_post_process(config['PostProcess'],
                                            config['Global'])

    # build model
    # for rec algorithm
    if hasattr(post_process_class, 'character'):
        char_num = len(getattr(post_process_class, 'character'))
        if config['Architecture']["algorithm"] in ['Distillation',
                                                   ]:  # distillation model
            for key in config['Architecture']["Models"]:
                if config['Architecture']['Models'][key]['Head'][
                        'name'] == 'MultiHead':
                    if config['PostProcess']['name'] == 'DistillationCTCLoss':
                        char_num = char_num - 2
                    # update character_num
                    config['Architecture']['Models'][key]['Head']['head_list'][
                        'CTCLabelDecode']['character_num'] = char_num
                else:
                    config['Architecture']["Models"][key]['Head'][
                        'out_channels'] = char_num
        elif config['Architecture']['Head']['name'] == 'MultiHead':
            if config['PostProcess']['name'] == 'CTCLoss':
                char_num = char_num - 2
            config['Architecture']['Head']['head_list']['CTCLabelDecode'][
                'character_num'] = char_num
        else:  # base rec model
            config['Architecture']["Head"]["out_channels"] = char_num

    model = build_model(config['Architecture'])

    use_sync_bn = config["Global"].get("use_sync_bn", False)
    if use_sync_bn:
        model = paddle.nn.SyncBatchNorm.convert_sync_batchnorm(model)
        logger.info('convert sync batch norm')

    # build loss
    loss_class = build_loss(config['Loss'])

    # build optim
    optimizer, lr_scheduler = build_optimizer(
        config['Optimizer'],
        epochs=config['Global']['epoch_num'],
        step_each_epoch=len(train_dataloader),
        model=model)

    # build metric
    eval_metric = build_metric(config['Metric'])

    # load pretrain model
    pre_best_model_dict = load_model(config, model, optimizer)

    logger.info(f"train dataloader has {len(train_dataloader)} iters")
    if valid_dataloader is not None:
        logger.info(f"valid dataloader has {len(valid_dataloader)} iters")

    # build engine
    engine = Engine(
        config,
        model,
        loss_class,
        optimizer,
        lr_scheduler,
        train_dataloader,
        valid_dataloader,
        eval_metric,
        post_process_class,
        pre_best_model_dict,
        logger,
        vdl_writer,
        use_visualdl=config['Global']['use_visualdl'])

    if config['Global']['profiler_options'] is not None:
        profiler_options = config['Global']['profiler_options']
        engine.profiler_train(profiler_options)
    else:
        # training
        engine.train()


if __name__ == '__main__':
    config, device, logger, vdl_writer = get_config()
    main(config, device, logger, vdl_writer)