import argparse
import runpy

MODULES = {
    'data-viewer': 'app',
    'tshirt-automation': 'tshirt_automation.app',
    'blueprint-review': 'blueprint_review',
    'product-reviewer': 'product_reviewer',
    'awakening-shirt': 'create_awakening_mind_shirt',
    'google-upload': 'google_drive_uploader',
    'fetch-products': 'fetch_shop_products',
    'creator-portal': 'creator_portal.app',
}


def main():
    parser = argparse.ArgumentParser(
        description="Unified command interface for Printify tools")
    parser.add_argument(
        'command', choices=MODULES.keys(), help='Which tool to run')
    args = parser.parse_args()
    module_name = MODULES[args.command]
    runpy.run_module(module_name, run_name='__main__')


if __name__ == '__main__':
    main()
