#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

## @author
import __future__
# given the webpage, we need to crawl the link

from typing import Set

from playwright.sync_api import sync_playwright, Page, expect, Browser, BrowserContext
from playwright.sync_api import TimeoutError

from bs4 import BeautifulSoup as Soup



from crawler.data_structure.manual_page_meta import ManualPageMeta


class MoparCarManualLinkCollector:

    def __init__(self):
        self.select_vehicle_url = 'https://www.mopar.com/en-us/my-garage/select-vehicle.html'

    def load_record(self, outfile):
        records = set()
        print('load records')
        with open(outfile, 'r') as file:
            for line in file:
                #print(line)
                line = line.strip() if line else line
                if line:
                    terms = line.split('\t')
                    if len(terms) == 4:
                        record = '{}\t{}\t{}'.format(terms[0], terms[1], terms[2])
                        records.add(record)
            file.close()

        return records

    def match_record(self, manual_page_meta: ManualPageMeta, records: Set):
        car_brand = manual_page_meta.car_brand
        car_model = manual_page_meta.car_model
        year = manual_page_meta.year
        record = '{}\t{}\t{}'.format(car_brand, car_model, year)
        #print('record matching: {}'.format(record))
        return record in records

    def crawl_link(self, outfile):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()

            try:

                page = browser.new_page()
                page.set_default_timeout(60000)
                page.goto(self.select_vehicle_url, wait_until="load")

                print('page loaded')
                brand_buttons = page.locator('button.box').all()

                manual_page_meta_collection = []
                for brand_button in brand_buttons:
                    brand_name = brand_button.get_attribute('data-make')

                    print('brand name: {}'.format(brand_name))

                    brand_button.click()
                    if brand_name:
                        # select year
                        year_options = page.locator('#ymmYear').locator('option.dynamic').all()
                        for year_option in year_options:
                            year = year_option.inner_text()
                            print('\t{}'.format(year))

                            print('\tclick "select year"')
                            page.locator('#ymmYear').select_option(year)
                            # page.wait_for_timeout('10000')
                            model_options = page.locator('#ymmModel').locator('option.dynamic').all()
                            for model_option in model_options:
                                model = model_option.inner_text()
                                print('\t\t{}'.format(model))

                                manual_page_meta = ManualPageMeta(car_brand=brand_name, car_model=model, year=year)
                                manual_page_meta_collection.append(manual_page_meta)

                        # print(select_html)
                        # soup = Soup(select_html)
                        # print(page.locator('#ymmYear').select_text())

                page.close()


                print('manual_page_meta_collection size: {}'.format(len(manual_page_meta_collection)))

                records = self.load_record(outfile)
                with open(outfile, 'a') as out:

                    for manual_page_meta in manual_page_meta_collection:
                        if self.match_record(manual_page_meta, records):
                            print('exist: {}'.format(manual_page_meta))
                            continue

                        car_brand = manual_page_meta.car_brand
                        car_model = manual_page_meta.car_model
                        year = manual_page_meta.year

                        print('start get link: ')
                        print(manual_page_meta)

                        page = browser.new_page()
                        page.set_default_timeout(100000)

                        page.goto(self.select_vehicle_url, wait_until="load")


                        brand_button_select = None
                        brand_buttons = page.locator('button.box').all()
                        for brand_button in brand_buttons:
                            brand_name = brand_button.get_attribute('data-make')

                            if car_brand == brand_name:
                                brand_button_select = brand_button
                                break

                        # brand_name match
                        if not brand_button_select:
                            continue

                        brand_button_select.click()
                        page.locator('#ymmYear').select_option(year)
                        page.locator('#ymmModel').select_option(car_model)

                        print('start to get the link of the specified car')
                        #page.wait_for_timeout(5000)
                        but = page.locator('input[value="Select Vehicle"]')
                        if but.is_visible():
                            print('select vehicle button found')
                            but.click()

                            print('clicked select vehicle')
                            #page.wait_for_timeout(5000)
                        else:
                            print('no more')

                        but2 = page.locator('a.link-arrow').get_by_text(r"OWNER'S MANUAL")
                        if but2:
                            print('Owner manual button found')
                            print(but2)
                            print('but2 visible: {}'.format(but2.is_visible()))
                            print('but2 inner text: {}'.format(but2.inner_text()))
                            but2.click()

                            print('owner\'s manual clicked')

                            #page.wait_for_timeout(10000)
                        else:
                            print('no more manual clicked')

                        but3 = None
                        manual_links = page.locator("#owners-manual-cta > a").all()
                        for manual_link in manual_links:
                            print(manual_link.inner_text())
                            if manual_link.inner_text() == 'EXPLORE THE MANUAL':
                                but3 = manual_link

                        if but3 :
                            print('but3 is visible: ' + but3.is_visible())
                            print('Explore the manual button found')
                            print(but3)
                            href = but3.get_attribute('href')
                            url = r"https://www.mopar.com" + href
                            print(url)
                            manual_page_meta.url = url
                        else:
                            print('but3 is None')
                            #print('but3 is visible: ' + but3)
                            print(but3)
                            print('url not collected')

                        out_line = "{}\t{}\t{}\t{}".format(manual_page_meta.car_brand, manual_page_meta.car_model, manual_page_meta.year, manual_page_meta.url)
                        out.write(out_line + '\n')
                        out.flush()
                        print('done')

                        page.close()

            except:
                print('error')
            finally:
                browser.close()

        return




if __name__ == '__main__':
    job = MoparCarManualLinkCollector()
    outfile = './car_manual_link'
    job.crawl_link(outfile)
