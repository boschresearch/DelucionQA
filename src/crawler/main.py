import hydra
from omegaconf import DictConfig, OmegaConf

import config.root_path as rp
from crawler.crawl_strategy.main_job_manager import JobManager

config_path = rp.getRootPath() / "config"
@hydra.main(version_base=None, config_path= str(config_path), config_name="config_crawl")
def main(cfg: DictConfig) -> None:

    print('-' * 20)
    print(OmegaConf.to_yaml(cfg))
    print('-' * 20)

    assert hasattr(cfg, 'input_url_file')
    assert hasattr(cfg, 'output_folder')
    assert hasattr(cfg, 'headless')

    crawl_param = {'headless': cfg.headless}

    job_manager = JobManager(input_url_file=cfg.input_url_file,
                             output_folder=cfg.output_folder)
    job_manager.run(crawl_param=crawl_param)

    return


if __name__ == '__main__':
    main()