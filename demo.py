from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select

from utils import parse_money, sign_in

if __name__ == "__main__":
    driver = sign_in()

    # navigate to Women >> Dresses >> Summer Dresses
    menu = driver.find_element(
        by=By.CSS_SELECTOR,
        value="ul.sf-menu.clearfix.menu-content.sf-js-enabled.sf-arrows",
    )

    ActionChains(driver).move_to_element(
        menu.find_element(by=By.TAG_NAME, value="li")
    ).pause(1).perform()

    summer_dresses_link = menu.find_element(
        by=By.LINK_TEXT, value="Summer Dresses"
    )
    summer_dresses_link.click()

    catalogue = driver.find_element(by=By.ID, value="layered_block_left")

    size_m_checkbox = catalogue.find_element(
        by=By.ID, value="layered_id_attribute_group_2"
    )
    size_m_checkbox.click()

    color_blue_checkbox = catalogue.find_element(
        by=By.ID, value="layered_id_attribute_group_14"
    )
    color_blue_checkbox.click()

    # hover over entry and click on More
    entries = driver.find_element(
        by=By.CSS_SELECTOR, value="ul.product_list.grid.row"
    )
    ActionChains(driver).move_to_element(
        entries.find_element(
            by=By.TAG_NAME,
            value="li",
        )
    ).pause(1).perform()

    more_link = entries.find_element(
        by=By.CSS_SELECTOR, value="a.button.lnk_view.btn.btn-default"
    )
    more_link.click()

    # select size
    size_select_element = driver.find_element(By.ID, "group_1")
    size_select = Select(size_select_element)
    size_select.select_by_visible_text("L")

    # set quantity
    quantity_input = driver.find_element(by=By.ID, value="quantity_wanted")
    quantity_input.clear()
    quantity_input.send_keys("3")

    # select blue color
    color_link = driver.find_element(by=By.ID, value="color_14")
    color_link.click()

    add_to_cart_button = driver.find_element(by=By.NAME, value="Submit")
    add_to_cart_button.click()

    sleep(1)
    confirm_box = driver.find_element(by=By.ID, value="layer_cart")

    # get size and color
    size, color = (
        confirm_box.find_element(
            by=By.ID, value="layer_cart_product_attributes"
        )
        .get_attribute("innerText")
        .split(", ")
    )

    # get quantity
    quantity = driver.find_element(
        by=By.ID, value="layer_cart_product_quantity"
    ).get_attribute("innerText")

    # get total product cost
    total_product_cost = driver.find_element(
        by=By.CSS_SELECTOR, value="span.ajax_block_products_total"
    ).get_attribute("innerText")

    # get shipping cost
    shipping_cost = driver.find_element(
        by=By.CSS_SELECTOR, value="span.ajax_cart_shipping_cost.unvisible"
    ).get_attribute("innerText")

    # get total cost
    total_cost = driver.find_element(
        by=By.CSS_SELECTOR, value="span.ajax_block_cart_total"
    ).get_attribute("innerText")

    assert parse_money(total_cost) == parse_money(
        total_product_cost
    ) + parse_money(shipping_cost)

    # display attributes
    header = (
        "| QUANTITY | SIZE | COLOR | TOTAL PRODUCT COST | SHIPPING COST | "
        "TOTAL COST |"
    )
    border = f"|{'-'*(len(header)-2)}|"

    print(border)
    print(header)
    print(
        "|----------|------|-------|--------------------|---------------"
        "|------------|"
    )
    print(
        f"| {quantity.ljust(9)}| {size.ljust(5)}| {color.ljust(6)}| "
        f"{total_product_cost.ljust(19)}| {shipping_cost.ljust(14)}| "
        f"{total_cost.ljust(11)}|"
    )
    print(border)

    driver.quit()
