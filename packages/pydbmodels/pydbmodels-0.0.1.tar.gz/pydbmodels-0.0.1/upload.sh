python -m pip install --upgrade pip && \
    python -m pip install --upgrade build && \
    python -m pip install --upgrade twine && \
    python -m build && \
    python -m twine upload -u __token__ -p pypi-AgEIcHlwaS5vcmcCJDM4NDNkMzFlLWQxOTItNDcwNy05NWI5LTVkODI2YjI3MzQwZQACKlszLCI5MjA0MDgzYS1hMGZiLTRiYzMtOTA3ZC02OGRkOWU0NWMyY2QiXQAABiDU4D6EddbVdTokmNDFTA_cwgS8Ip1dsh-CQt2q98c6Dg dist/*