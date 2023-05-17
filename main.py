from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from utils import parse_money, sign_in

if __name__ == "__main__":
    driver = sign_in()

    # click on BEST SELLER link
    best_seller_link = driver.find_element(
        by=By.CSS_SELECTOR, value="a.blockbestsellers"
    )
    best_seller_link.click()

    # get list of products
    product_containers = driver.find_elements(
        by=By.CLASS_NAME, value="product-container"
    )

    # variables to track width of columns when formatting output
    max_label_width = 0
    max_price_width = 0

    # dictionary to store the product labels and prices
    products = dict()

    # iterate over products and get label and price of eact product
    for container in product_containers:
        # get the label text
        label_text = container.find_element(
            by=By.CSS_SELECTOR, value="a.product-name"
        ).text

        # update the maximum label width if surpassed by current label
        max_label_width = max(len(label_text), max_label_width)

        # get the price text
        price_text = (
            container.find_element(
                by=By.CSS_SELECTOR, value="span.price.product-price"
            )
            .get_attribute("innerText")
            .strip()
        )

        # update the maximum price width if surpassed by current price
        max_price_width = max(len(price_text), max_price_width)

        # get the price value
        try:
            price_value = parse_money(price_text)
            products[label_text] = price_value
        except ValueError as error:
            print(error)

    sorted_products = sorted(products.items(), key=lambda product: product[1])

    ##########################################################################
    # FORMAT AND PRINT TABLE                                                 #
    ##########################################################################
    print("BEST SELLERS\n\n")

    header = (
        "| LABEL".ljust(max_label_width + 2)
        + " | PRICE".ljust(max_price_width + 4)
        + "|"
    )

    border = f'|{"-" * (len(header)-2)}|'

    divider = f'|{"-" * (max_label_width + 2)}|{"-" * (max_price_width + 2)}|'

    print(border)
    print(header)

    for label, price in sorted_products:
        print(divider)
        print(f"| {label.ljust(max_label_width)} | ${price:.2f} |")

    print(border)

    ##########################################################################

    # navigate to Women >> Dresses >> Evening Dresses
    menu = driver.find_element(
        by=By.CSS_SELECTOR,
        value="ul.sf-menu.clearfix.menu-content.sf-js-enabled.sf-arrows",
    )

    ActionChains(driver).move_to_element(
        menu.find_element(by=By.TAG_NAME, value="li")
    ).pause(1).perform()

    evening_dresses_link = menu.find_element(
        by=By.LINK_TEXT, value="Evening Dresses"
    )
    evening_dresses_link.click()

    catalogue = driver.find_element(by=By.ID, value="layered_block_left")

    size_m_checkbox = catalogue.find_element(
        by=By.ID, value="layered_id_attribute_group_2"
    )
    size_m_checkbox.click()

    color_pink_checkbox = catalogue.find_element(
        by=By.ID, value="layered_id_attribute_group_24"
    )
    color_pink_checkbox.click()

    price_range = catalogue.find_element(
        by=By.ID, value="layered_price_range"
    ).get_attribute("innerText")

    # slide the range selector until required range is obtained
    while price_range != "$50.00 - $52.28":
        slider_handles = catalogue.find_elements(
            by=By.CSS_SELECTOR,
            value="a.ui-slider-handle.ui-state-default.ui-corner-all",
        )
        ActionChains(driver).drag_and_drop_by_offset(
            slider_handles[1], -4, 0
        ).perform()

        price_range = catalogue.find_element(
            by=By.ID, value="layered_price_range"
        ).get_attribute("innerText")

    driver.quit()
