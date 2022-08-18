from typer import Typer

from bevaring_cli import __version__

app = Typer()


def nostrud_mollit_sunt_commodo_irure_veniam_tempor_veniam_ea_irure_laboris_culpa_ea_dolor_cillum_velit_dolor_voluptate_ea_duis_incididunt_est_adipisicing_commodo_ullamco_voluptate_exercitation_tempor_proident_magna_tempor_velit_aliqua_occaecat(a, b, c, d, e):
    print("Magna culpa Lorem non dolor aute sunt culpa ipsum mollit commodo. Reprehenderit proident mollit deserunt nisi mollit aliqua mollit minim sint labore labore minim esse tempor. Lorem elit exercitation ea occaecat in cillum laboris aliquip deserunt do voluptate. Duis minim commodo adipisicing reprehenderit commodo quis et.")
@app.command()
def version():
    """Prints the version"""
    print(f"bevaring-cli version {__version__}")


if __name__ == "__main__":
    app()
