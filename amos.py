# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class Amos:
    def __init__(self, drvier, input_dict):
        self.driver = drvier
        self.input_dict = input_dict


    def auto_process(self):
        self.driver.get('https://docs.google.com/forms/d/e/1FAIpQLScyC2izxDvE9WSSdY8eLFIus-kedcdQrdW9UB4LCL0ku6JmjQ/viewform')
        element = WebDriverWait(self.driver, 30, 0.5).until(
            EC.presence_of_element_located((By.ID, "mG61Hd")))

        #1.input every para
        inputs = self.driver.find_elements_by_tag_name('input')
        for input in inputs:
            if input is not None:
                label_name = input.get_attribute('aria-label')
                if label_name is None:
                    continue
                time.sleep(1)
                try:
                    input.send_keys(self.input_dict[label_name])
                except:
                    print('Input fail : ', label_name)

        # labels = self.driver.find_elements_by_tag_name('label')
        # for label in labels:
        #     if label is not None:
        #         time.sleep(1)
        #         checkbox = label.find_element_by_tag_name('span')
        #         ActionChains(self.driver).move_to_element(checkbox).click(checkbox).perform()


        button = self.driver.find_element_by_xpath("//div[@role='button']").find_element_by_tag_name('span')
        button.click()



if __name__ == "__main__":
    import xlrd
    import configparser
    from dial_adsl import Adsl

    cf = configparser.ConfigParser()
    cf.read('config.ini')

    username = cf.get('adsl', 'username')
    password = cf.get('adsl', 'password')
    print(username, password)
    adsl = Adsl(username, password)

    input_file = cf.get('input', 'file')
    book = xlrd.open_workbook(input_file)
    sheet = book.sheet_by_index(0)
    print(sheet.name)

    for row_index in range(1, sheet.nrows):
        driver = webdriver.Chrome()

        wallet = sheet.cell(row_index, 0).value
        email  = sheet.cell(row_index, 1).value
        input_para = {}
        input_para['Eth Wallet address 錢包地址 '] = wallet
        input_para['Email'] = email

        with open('result.txt', 'a') as fw:
            try:
                shop = Amos(driver, input_para)
                shop.auto_process()
            except:
                fw.write("ERROR: " + wallet + ',  ' + email+'\n')
                print("ERROR: " + wallet + ',  ' + email+'\n')
            else:
                fw.write("SUCCE: " + wallet + ',  ' + email+'\n')
                print("SUCCE: " + wallet + ',  ' + email+'\n')
            finally:
                driver.quit()

        adsl.dial()


