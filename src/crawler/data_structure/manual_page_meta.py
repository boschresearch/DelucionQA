#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

## @author Bingqing Wang
import re
from typing import List, Optional

from pydantic import BaseModel

class ManualPageMeta(BaseModel):
    car_brand: Optional[str] = None
    car_model: Optional[str] = None
    year: Optional[str] = None
    url: Optional[str] = None
    chapter: Optional[str] = None
    section: Optional[str] = None
    sub_sections:list = []

class UtilityManualPageMeta:
    @staticmethod
    def get_manual_hubpage_url(manual_page_meta: ManualPageMeta):
        year = manual_page_meta.year
        car_brand = manual_page_meta.car_brand
        car_model = manual_page_meta.car_model
        hubpage_url = "https://www.mopar.com/jeep/en-us/my-vehicle/explore-the-manual.html?year={}&brand={}&model={}".format(year, car_brand, car_model)
        return hubpage_url

    @staticmethod
    def get_manual_hubpage_url(manual_page_meta: ManualPageMeta):
        url = manual_page_meta.url if manual_page_meta and manual_page_meta.url else ''
        return url

    @staticmethod
    def get_store_path(manual_page_meta: ManualPageMeta):
        '''

        :param manual_page_meta:
        :return: return two path: path_html and path_html_individual
        '''
        car_brand = manual_page_meta.car_brand
        car_model = manual_page_meta.car_model
        year = manual_page_meta.year
        chapter = manual_page_meta.chapter
        section = manual_page_meta.section

        html_folder_given_car = car_brand + '/' + car_model + '/' + year
        path_html = html_folder_given_car
        path_html_individual = html_folder_given_car
        if chapter and section:
            path_html = '{}/{}/{}.html'.format(html_folder_given_car, chapter, section)
            path_html_individual = '{}/{}/[STANDALONE]_{}.html'.format(html_folder_given_car, chapter, section)
        else:
            path_html = '{}/hub.html'.format(html_folder_given_car)
            path_html_individual = '{}/[STANDALONE]_hub.html'.format(html_folder_given_car)

        return path_html, path_html_individual

    @staticmethod
    def load_from_tab_file(infile_path: str) -> List[ManualPageMeta]:
        ret_list = list[ManualPageMeta]()
        with open(infile_path, 'r') as infile:
            lines = infile.readlines()
            for line in lines:
                line = line.strip() if line else ''
                terms = line.split('\t')
                if len(terms) >= 4:
                    car_brand = terms[0]
                    car_model = terms[1]
                    year = terms[2]
                    url = terms[3]
                    mpm = ManualPageMeta(car_brand=car_brand, car_model=car_model, year=year, url=url)
                    ret_list.append(mpm)
            infile.close()

        return ret_list

    @staticmethod
    def clean_chapter_section_title(manual_page_meta: ManualPageMeta):
        chapter = manual_page_meta.chapter
        section = manual_page_meta.section

        if chapter:
            chapter = re.sub('<[^<]*>', '', chapter)
            manual_page_meta.chapter = chapter

        if section:
            section = re.sub('<[^<]*>', '', section)
            manual_page_meta.section = section

        return