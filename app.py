from click_web import create_click_web_app
import cli

app = create_click_web_app(cli, cli.cli)
