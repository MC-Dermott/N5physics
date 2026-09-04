import random
import math
import pathlib
from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question

G = 9.8  # m/s²

_SLOPE_WIDGET_HTML = (
    pathlib.Path(__file__).parent.parent.parent / "core" / "data" / "slope_forces_widget.html"
).read_text(encoding="utf-8")


def _with_slope_widget(question):
    question.metadata["widget_html"] = _SLOPE_WIDGET_HTML
    question.metadata["widget_height"] = 900
    return question

_COMPONENTS_DIAGRAM_B64 = (
    "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"
    "aMN+A13Aywn3lTvWucYa912xfpHvPZd1u2bXL6qfH+Vq6QR7IPR+/nadfb3PQBfoV62zzT36lvnVkG3984E2lJ4+O6+x3G418Olf"
    "9oab2EeTOsYTbf86x+WR67TnnmssW4KPg9ZYtoQA/9q33NdHeF28Za2/F/WL55f6litfUHeb0z7a7Gt3ou/VRXh/1efUW/6X6/VM"
    "HNj+5cd9T/mxD7wG8tz2gZ3vDeg1sBoBQrla856Bnw+vMQ7x3Drh0XrbPHrYL851+Vv3Lf/fA797RN/vnjDmc9x+YE6CV3Qs/6e1"
    "e21v+YeM+WW+vxvv+zZ4vG3qFeUNv2CMGSB0DU14fd+yL17j9xcZCAUe3bG9u0wyQBjxOD95s6+VcQKEKb2+Bo9j5/OpV/n638vr"
    "zivSsZ3X9m3npUMsf/G+se5ndIV8Ew4QNgwsIuLQvmW/MsEA4d/71vnaRuPU6xXYY/qW/9dNvCYndYwn2v41jsurOx5/cMjCzTZY"
    "9tJ93dnPW+dL/ODjdz2nS9bwrrf8Q+ewjybx2p3oe3UR3l91otwN/875sQ+8BvJK7ANlHGE1lCEKdx74uXVfl+6o3UvL+MlyNWa9"
    "rvhl9uXi6JzzB7seNOf8kdoVvrhh7crcU7ph9tyrdmkf1bVqN/uoV9yf19Ge0l2///mVmbfHUcKZ3rCF29YunWu5ZT1JLo7JOZer"
    "RJNQQok1j1Of3pCI3vFfa9/1uvuWL8kXVgNYT875PbWnyjyUE/6e0mV3Vqb9+ipjltfsYt1Tu/2W4UA9z8w5l+M1jtKbo6eMrd5Q"
    "zrm8d8t7OGo39Vnu+3aTr++R1ZnhS9WDnudsNDypVhsoPVR6blmP16iPO5FjPKP2lwk/N1KGW/SUXgWf3ODxf9LXrX7bvs/KjTy/"
    "4zmVIVGvW+89OKN9NInX7rTfqzN/f9UeWr0KHQenlMqwE2AFKeMIW8M59cSv/+RvUBnq0F+yqXQ/7emdUPWfWPX+3xsXXsbq/lHt"
    "0lp8uv7cpJYCOyGl9NE6nKGMMT8y51yuqGykrNfztXoS1eU/61CM3hfEkZUyYSmlD9e5IHaocw6UyRUH9c87USb1mpRyRejCSzob"
    "KCfSPWXiy4323afXmiNhnZPKEiRNVEppnzrXwn71StquA39/enNzFH8cszPt19eX1yp5N6DM1dALqM6vk52OLKVU5nAo+7n3fn9F"
    "3/egtd63vX8P6PvdUOVdJ+DXOecyp8pGerPHp3Ve3+Mow1B68zOUL5Xl82iY492zV/2yVXoQjGIix3gG7T855zw4X8ig/vfIV4Z4"
    "/F/U0o4xxHG8YOCL7Xr+q85tstZ7cNr7aNOv3Rm8V+fy/ipz/6SUSgD1tDp/w1dSSp8rvRPra+WInHPv/ABYYgIEWA2frCWZenau"
    "JxilPNS165fgp9UTudJ1cS2la2hPuVJ09zHaUa54X3iCUL4Ap5RuX794H1LbdMf6U5RJl46okza+sV6tGlQCiZ7+CRk30n8VfZxe"
    "D/2BQG8yyfsMBgi1Tvn/PZda0nJSytCDLud3fJb3P/euLwU9vauFE5FSKifzL6lXX4e9cltOPGdl2q+vE4fYXglUoq9++4Y16TfQ"
    "//7dYRPv31nofH3Xz4/yvtp2gucq/cf7xCHCndKOX6aUSnv37DvmowYIkzrG027/b0f83Bl1+a7j+MshQuXele713oPT3keTeO1O"
    "+706r/dX1Lkcyrwvf1ODnBvXnwullH5YJw5903qTSwKLzxAGWA0nlC7ofT9vyTk/L+d8nXqVvDcD+SEppfVm1p/EVYheVYYLlRPl"
    "nPO9a3BRZpwuwyJO6vv8KVePnl1OCFNK5cRjUP+V6d+rbLCBM9dZf5xu9WXm6OJaKaUyvrPf3fu2//F1ApB56p+9vZzQDaPzZHtY"
    "tftqmfCsVJwYpdt3r7rELEz79TVMr48SrE1i/0/8/buCxjneg8v2H69hTeoYz6v9s3LWBN6Dy7CPVva9WoKJnPPz60WI+9bhgL05"
    "JqKeC5RzkK+mlN5Vq+AAS0YPBFhxpdRcLan41HrXi0qJqzW6EvZfTfp4RPzjGA+3Zhm4nPMJ9Ur0heNrU0qld8RN61wNt69XYZ6Z"
    "Uip1z/vHg/ZfqetdHerSv9y4V/pKm89NKZXx7o/s64XwxL5Fet3YJz18YVL6r+TtPocr0G/s214JsD5bJ2D7cb1CdnZfsLVX1xwN"
    "UzK319c6VwvXm2tjGP3v3/LeftQY2yg9glbZyMe7joffY8Sr7tM6xvNq/6zsMcZypyzhPlr592rtZfOm3t/GlNIedZjk7WovyNI7"
    "4a61EsZt5t1eYDQCBNganlNLcF2xXl15ZkQ8eIMv/zvWSfWmIuf843pl4m0ppTL7/7vrr55cxlD2TXr1k3XGq2+kf+Kmn0zgS3Av"
    "QDg0pfTknPP5NZC5Ub3/lE2MaZ6m/ud+jSHXKTXCNy2ldEDfY5aJBG+Zc/7SBstP5HHHMO/XV1HCtZ69UkqljGV/F+1h9b9/y8SQ"
    "Hxqm+/YW03+8Lp5SulTOuWuYyVUGrkj/dI7HeF7tn5XdU0qXq4HzRq65wXtwGfbRlnuv5px/W4cufCil9NIaJpdQ4dYppWsZzgDL"
    "xRAG2AJyzmWipqf33XW/chI7sNj/9P2/VFS4yoza9p6+ibnKCUV/u77Q9/99U0plPocu/XM8bKoqQs65XOX5Zt+41VLZYnDyxFL2"
    "a9iut7NUTtD6j+elNlo4pbTzwEzxm9Gr5lF8YKPwoK+axTzM9fVV1IkbS/nUngeNuZ2T+uZnuEidd2TVlbK0Q5/P1GFGJbzsKZOj"
    "jnK8vzdO9YQJHuO5tH/G7jHiMqVk61LtoyV6r470/hpWzvnYgckth/ncBRaIAAG2jlJV4Tt9vY+esUZ5rI/2fTa8pU4U2CmlVL58"
    "3WLgvtvVoQoxxBfXNcec1qt03+i761UppR022NZ9+3oGFO+NzesfnnCf2t31sHV+vzByzt8bON7lqk9XL5VJjUftn/Ngw22mlC5f"
    "J9yauQV5fRVv6fv/Y1NKNx9zO2/u+/8LUkql6kWn0r04pTTMF7dFc0bfMJhy9bp/3o/1vK/v/09JKV12vQXr/nvchI73pI7xvNo/"
    "K0/ueE4lbLxTx3Nahn20DO/Vkd5fZd6blNL1h9x2/2SXwJIRIMAWkXMuJwLP6rurTKjYf6W4eEotfVVct050dOeU0h9MbFfuKyfB"
    "KaUyFOHbA2Ugo17NPial9M8ppVIT+g+GTNVeEO/sK7t16hqzX/fXsy4nJx8pgcXAdnZIKT1+oD54Kcs3TEmwLm/ruxJz+zpvQ++E"
    "9Ls559+7ArZgXt73/7unlN6aUvq9E7eUUinZ+bKBk+jN6r/aetuU0uNSSr832Vl5PaSU7l6v4s/zZHLer6+oFVR6ZTnLe+3DKaW/"
    "WSvASyltk1K6UUqpTD466JV9XbjLWPvPp5TKl9U/GFtegrAydCSl9OI6q/0DYsnUUqc/7DufKcO0uryib3LLsl8+nVIqJUZ/T0rp"
    "r2qvrN7r9vSI+PsFOMbzav+slOf0qZRSKf87uE9KcPv+voDyW7Wk4zLuo4V/r47x/ipVd75QSiCnlO6UUtplcIGU0sVSSs+NiP4A"
    "rT/EBZaAORBga3l3nUxx/3pCUOZC+L+rGTnnEhg8om9Cu/JFqgwxOD2ldFQps1Vnfy5f+K4+xCz05YrF/erP71JK36rbKOv9cURc"
    "bWD5V+Wcf2/m+pzzv5QQo++qUznx+F5K6Zt1LOkutZrD7gNXTvp7CYytlvj6cA0PLjIwuWT/VaRF9PraPbd3Mn5oDRJK+axf1PG3"
    "pfto78rSN/vmLuhdeRpZzvnIWqLzwHqyXybPfHo9/qWyxR51HHPvZLm37MzN+/VV23BaSqlMKPaJ+uWyvM7KTObPSil9o37xvEit"
    "HV/Cq/Kl8+yBYUllO+V9eofyham2e/fa86RNKX2nju0+tx73q21yQr9FUb4AljlJijeklB5TQ8j+7tf3LJOilv/knI9LKT2xfoEr"
    "LlcmjU0pHV+Dr1Q/28os8v0etpka9hM8xnNp/4z8qgbYl68hQvmy/L16rnrAQDnMstz96pfcWLZ9tETv1ZHeX9Wt68959TO/t08v"
    "Xs89+nt5fW7BQ3hgLeWz14994DWwfK+BemU81583jbDenfrWK18S919jmRIqnNa3XNdPOSm7/sA2yszKx42wjX8pJ9brtHmnGmQM"
    "s50SUNxwg+d/y75l/2PIfXbHNR6nnMD+8ZDrdz5mnVeht8zrh9jmwX3Lf3yD5cqJ59eH2G8lDHlo3+0XbPL1uX+dfb7rcctcDfv1"
    "3f7uBN4bX+zb3rWHWH6Sr6+RjuPAujepwc4w7Thrg+2UcObYEd57J9cvY+Pu7+36tvW7dZa5fN8y3x9yu+f13msbLHO1WoJvo+e3"
    "4xrrPbl+/nXtm9KGh272NTmFYzyR9o96XGo53t7yLxxi+c/2LX/9rsevPdlO6XhOZU6fOw3x2HPZR8O+dif5Xl2E91cNGj4zwnMp"
    "Ie2lJvXe8mMfeA3kme0DQxhg6/m3vhJQaWBYw4Vyzv9aTwZeUEOAtZSTinJl/m7las7gVYSc84drl8ZD61W3/isUPRfUKzB3zjnf"
    "a+AqRv+2ymPdtf58eZ2r4+WkvHTF3y/nvOnJ7Qb8Z/3i2O9jOedFntH8QnVCsDJu/9n1Ct+gcoXvATnn+0yyRGHO+ah65b683s5f"
    "Y5Hj65CZGw2UnJy5BXh99dpR3gtXqfNRDA7l6Tm/nqQ/dYPtfKMGOA+t4dFaz6fc99WIeHSpzZ5zfkMsoZxzCS9vMTAh5jDrvTAi"
    "rhMRHyxf1NdY5IwaKh2Qc37NAh7jubR/2up764A6VKEEBYP7pQxZOCjn/L4htrXw+2jR36ujvL9yziW4uHHtxfWODT7XyzbLkLDr"
    "DFEhA1hAqaaGwJJJKV2nds0sji/DD0ZYt5zA9krnlQ+Bf6tzJKy3/KXrFY4960ndz8u8B+t94V9nGzvX7vEXr1c+ypfZ7+ScS5m/"
    "kaSU9q4n4aV7Z/nyV05Cjl6rO+sa6168r0v/STnnzw35mDeowy56jqoTFcYkHrOUL6snu8VxXWWtUkp79Y0j/XnO+TNDtGPbegwu"
    "VU+of1RnxO79/p01ECrunnN+1zDPb4jHvWi90naxelL505zzMX2/36mvAsSpOeePbvLxbt7X5fe/c86/meHra6Tj2LGt8p67XO3e"
    "fEoNMX486numjqu+St0n29T3Xnn/ll5Gm1YnFi3DQKJezXz/Ou//v6w3Sy+Fjwyx3TvV9l4wzBfGetzKFdM96nCAnvd1fL6V19+f"
    "1s+mXPfztwaHU03DJI7xZto/6nFJKV25b5hT6S30rY7lbxYR5bgUn8g5/3qN598LqX+Qc77SwOv2qnXI3Cn178VaIehC7aNxXrub"
    "fa8u4vur/r350/p3s/RS+m19zQyG8cCSESAA0PuSXyb12q3ujn3LFSW7BpjaSegGAQIAi8kQBgCiTnTYCw/K1XbhAQAAv0eAALDC"
    "Uko3LOXPavfTtX5/xZTSuwZKg/WqcAAAwP9RxhFgtZUxy28s435TSj+u5eJ+UUvJXaH+vl+ZyOsf5tRWAAAWmAABYGtItb58+VnP"
    "kWUyw5xzmeQSAAB+jyEMAKutVHx4U+15sJ5STeJxtU77RssBALCFqcIAsEWklC5Vy5iVsmilrNmva6nBn867bcDWM075QQDmS4AA"
    "AAAAdDKEAQAAAOgkQAAAAAA6CRAAAACATgIEAAAAoJMAAQAAAOgkQAAAAAA6CRAAAACATgIEAAAAoJMAAQAAAOgkQAAAAAA6CRAA"
    "AACATgIEAAAAoJMAAQAAAOgkQAAAAAA6CRAAAACATgIEAAAAoJMAAQAAAOgkQAAAAAA6CRAAAACATgIEAAAAoJMAAQAAAOgkQAAA"
    "AAA6CRAAAACATgIEAAAAoJMAAQAAAOgkQAAAAAA6CRAAAACATgIEAAAAoJMAAQAAAOgkQAAAAAA6CRAAAACATgIEAAAAoJMAAQAA"
    "AOgkQAAAAAA6CRAAAACATgIEAAAAoJMAAQAAAOgkQAAAAAA6CRAAAACATgIEAAAAoJMAAQAAAOgkQAAAAAA6CRAAAACATgIEAAAA"
    "oJMAAQAAAOgkQAAAAAA6CRAAAACATgIEAAAAoJMAAQAAAOgkQAAAAAA6CRAAAACATgIEAAAAoJMAAQAAAOgkQAAAAAA6CRAAAACA"
    "TgIEAAAAoJMAAQAAAOgkQAAAAAA6CRAAAACATgIEAAAAoJMAAQAAAOgkQAAAAAAECAAAAMDm6YEAAAAAdBIgAAAAAJ0ECAAAAEAn"
    "AQIAAADQSYAAAAAAdBIgAAAAAJ0ECAAAAEAnAQIAAADQSYAAAAAAdBIgAAAAAJ0ECAAAAEAnAQIAAADQSYAAAAAAdBIgAAAAAJ0E"
    "CAAAAEAnAQIAAADQSYAAAAAAdBIgAAAAAJ0ECAAAAEAnAQIAAADQSYAAAAAAdBIgAAAAAJ0ECAAAAEAnAQIAAADQSYAAAAAAdBIg"
    "AAAAAJ0ECAAAAEAnAQIAAADQSYAAAAAAdBIgAAAAAJ0ECAAAAEAnAQIAAADQSYAAAAAAdBIgAAAAAJ0ECAAAAEAnAQIAAADQSYAA"
    "AAAAdBIgAAAAAJ0ECAAAAEAnAQIAAADQSYAAAAAAdBIgAAAAAJ0ECAAAAEAnAQIAAADQSYAAAAAAdBIgAAAAAJ0ECAAAAEAnAQIA"
    "AADQSYAAAAAAdBIgAAAAAJ0ECAAAAEAnAQIAAADQSYAAAAAAdBIgAAAAAJ0ECAAAAEAnAQIAAADQSYAAAAAAdBIgAAAAAJ0ECAAA"
    "AEAnAQIAAADQSYAAAAAAdBIgAADAEkgppXm3AdjaBAgAAABAp5Rz7l4KAAAA2NL0QAAAAAA6CRAAAACATgIEAABYoIkSTZYILCoB"
    "AgAALJBskjJgQZlEEQAAAOikBwIAAADQSYAAAAAAdBIgAADAjJgkEVhmAgQAAJghkyQCy8okigAAAEAnPRAAAACATgIEAAAAoJMA"
    "AQAAJshEicCqEiAAAMCEmSgRWEUmUQQAAAA66YEAAACbYMgCsFUIEAAAYBPhQfnXkAVgKzCEAQAARj2JTqmcR2c7DthK9EAAAIAx"
    "eh0AbDV6IAAAwDAnznodAFucHggAANBBrwMAAQIAAGzIRIkA/8sQBgAAWIMhCwC/zxAGAAAYYMgCwB/SAwEAAHonxyZKBFiXHggA"
    "AKDXAUCn7boXAQCArTFcIeec59sagMUlQAAAYMsyZAFgeIYwAAAAAJ1MoggAwJYcsmC4AsBo9EAAAGDLEB4AjE+AAADAlqLnAcB4"
    "DGEAAGCl6XUAMBl6IAAAsPL0OgDYPD0QAABYOXodAEzedlPYJgAAzDU4KPQ6AJgsAQIAACtBrwOA6TIHAgAAS094ADB95kAAAGDZ"
    "goJ9IuLK9We/iLh5ROxbF/l1RDwq5/y+OTcVYOUIEAAAWDgppT1rQLBvX1jQ+9lliE28MOf8NzNoKsCWIUAAAGBuUko7RsStIuLq"
    "AyHB3pvcdI6IK+WcfzihpgJseSZRBABgLlJK94mIl0fEHtPYfETcMyKeN4VtA2xJAgQAAGYupXSniHjTlB+mNy/CH2ia5hIRcbuI"
    "eF/btmXeBAA6qMIAAMA8PGUGj/Gva93ZNM2rIuJnEfFPEXFy0zTPnEFbAJaeORAAAJi5lFKZo2CaTi1DI3LOv/c4TdNcJyK+vMby"
    "V2zb1nwJABvQAwEAgHk4d8rbP2QwPKhetM7y690PQCVAAABgHt45xW1/LOf8H4N3Nk1z1Yi42Trr3KFpmktPsU0AS0+AAADAPDw3"
    "Is6a0raftM79T6vVGdayfUQ8eUrtAVgJAgQAAGYu5/y9iHjiFDb99pzzEev0PihlHTfyQL0QANYnQAAAYF5eHRH/NcHtnVN7GYza"
    "+6BnB70QANYnQAAAYF72Lp0RJri9f8g5Hzdm74MevRAA1iFAAABg5lJKt4mIoyLi1hMs2/i8TfQ+6NELAWAdAgQAAGYmpbRzSqkM"
    "XfhQRFxigpt+Uc75V5vsfdCjFwLAGgQIAADMRErp2hHx9Yh42IQ3fVJEvHwCvQ/6eyE8ZgLtAlgpAgQAAKYqpbRdSukpEfGFiLjK"
    "FB7iGTnnMybU+6DnZptvFsBq2W7eDQAAYHWllP4kIt4aETec0kN8NyLeOMHeB/29GgDoowcCAAATl/7X/SLiG2OEB+eNsOyTc87n"
    "Tbj3we/KnApjrguwsgQIAABMVEqplGd8b0T8c0TsOuLqH6zDB84aYtnP1+Un3fvgdW3bfnbMdQFWVsp5kqV3AQDYymp5xjdExCVH"
    "XPX0iHhsRLw+55xTSo+IiFd1rHNwzvlzg3c2TXO1iPhOjO/XEXH5tm1P28Q2AFaOHggAAEy6POOo4cGXIuKAnPM/lfCg3le29ZEN"
    "1nnnWuFBtZnwoLhYRJQAA4A+eiAAALApKaVrRcTbx6iwcH5EPCcinrfWPAYppd0j4j9KT4OBX30lIm6Rcy5zFfyepmnKJOHnxubp"
    "hQAwQBUGAADGklLatkxiGBHPHOO88tiIOCznXHofrCnnfEpK6VYRcceI+MuIOCciPhUR71grcKguEuMpQy8G5z04c8xtAawkPRAA"
    "AJh1ecZ/jIjH55zLvAcT1zTNOJN83axt2xJOALAOPRAAABhaqc0YEYdHxCvHqLDwi4h4QM7536e8y0svhF9FxG71dum5cEz9f7nv"
    "clN+fICVJEAAAGCU8oyvi4i/HmOX/XsND0qIMFVt25bA4KJr/a5pmv0j4ptr/OoH024XwLJThQEAgGHLMx41RnhwRkQ8KCLuMIvw"
    "YAjfiojB6g3/0bbtT+bUHoClIUAAAKCrPOPfT7A841y1bZvrhIyl+sN/RsTTI+Ku824XwDIwiSIAABuVZ3xbRFx1kuUZAVhO5kAA"
    "AGCS5Rm/HxGHblSeEYDlJEAAAOD/pJSuUMsz3mjRyjMCMF8CBAAANlue8ZcRcf8ZlGcEYI4ECAAAW1wtz1h6D9xpkcszAjBfqjAA"
    "AGxhKaVb1/KMd1ry8owATJkeCAAAW7Q8Y6lqGBEPH2P1MkHiYTnnY6fQNAAWlB4IAABbTErpoIj42hjhwfm1MsPBwgOArUcPBACA"
    "rVWe8UkR8SzlGQEYlQABAGAL2GR5xtfV8oy/m0LTAFgShjAAAKx4ecaUUinP+I0xwoNSnvH2OecHr2J40DTNRefdBoBlknLO824D"
    "AACLV57xP2p5xp/Himma5oYR8ZaIuGJEHB0R92zbtgQsAGxAgAAAsIJSSn8REW+KiEuOUZ7xsRHxT3kFrzQ1TbNTRPwsIvp7H5wU"
    "EZdp27ZMEgnAOgxhAABYsfKMKaVXRcRHxggPvhwRB+ScX7eK4UF1/YHwoNgnIvafU3sAloYAAQBg9cozPmLEVc+vlRm2QnnG9eY9"
    "2H3G7QBYOqowAACsRnnGJiKerTwjANMiQAAAWP7yjGVCwIPHWP2fIuJxq1hhAYDJEyAAACyhUpsxIu4dEWW+g93GKM9YKix8cErN"
    "A2AFCRAAAJZMSmmvWp7xzmOsvrLlGQGYLpMoAgAsX3nGo8YID0p5xodExO2FBwCMQw8EAIAlkFLaKSJeFBGPHGP1Up7xsJzzMVNo"
    "GgBbhB4IAADLU57xkZsozyg8AGBT9EAAAFjN8ow/iIhDc85fnFLzANhiBAgAAAtIeUYAFo0AAQBggSjPCMCiEiAAAKxGecb/jIj7"
    "q7AAwLSYRBEAYDXKM95OeADANOmBAACwvOUZv1InSlRhAYCp0wMBAGD5yjNeUCsz3Eh4AMCs6IEAADCf8oxPrCHA9iOurjwjAHMh"
    "QAAAmKGU0uUj4i0RceMxVn99RDw25/y7KTQNADYkQAAAWPzyjL+qFRY+OKXmAUAnAQIAwGzKM742Iu4yxurKMwKwEEyiCAAwRSml"
    "P6/lGUcND86MiIcqzwjAotADAQBgeuUZXxgRjxpjdeUZAVg4eiAAAExYSunAiPjqGOGB8owALCw9EAAAFqc842E55y84IAAsIgEC"
    "AMAEKM8IwKoTIAAAbL4842ER8fdjlmd8QM75Aw4CAItOgAAAMKaU0sVqeca7jrH6hyLi/jnnnzkAACwDkygCAIwhpXSrWp7xrmOW"
    "Z/wr4QEAy0QPBACA2ZVnLJUZDs05f89On5szRrwfgEoPBACA2ZRnfE5E3FB4MHdfjIizB+77bUQcOaf2ACwNAQIAwBDlGVNKT4qI"
    "L0XEfmOUZzw45/z0nPO5dvZ8tW17WkTcOSJOqXedHBF3aNvWsQHokHLOXcsAAGxZyjOupqZpylDePykBT9u258+7PQDLQIAAALB+"
    "ecZDa3nGi45RnvGBOef327kArAqTKAIADFCeEQD+kDkQAAAmV57xYcozArCq9EAAAPj/5RlfEBGPHmOHKM8IwMrTAwEA2PJSSgfU"
    "EGDU8EB5RgC2DD0QAIAtXZ4xIh4fEc+NiO1HXP2HEXFYzvnzU2oeACwUAQIAsCWllC4XEW+JiJuMsfo/R8Rjc86nTaFpALCQBAgA"
    "wJaiPCMAjEeAAABsGZssz/jhiLhfzvlnU2gaACw8kygCAFtCSumWmyzPeFvhAQBbmR4IAMBKU56RQU3TXCQiHhARB0bElyLijW3b"
    "nmdPAWxMgAAArHp5xrdHxH5jlGd8fkQ8O+d87pSaxxw0TZMi4t0Rcbt61/0j4uCIuI8DArAxQxgAgJUsz5hSaiLiy2OEB6U8441z"
    "zk8THqykK/eFBz33bprmEnNqD8DSECAAAKtYnvETEfGiiNh+xNXfEBEH5Jw/P6XmMX9XHfF+ACpDGACAlbDJ8ownlzHxOef3T6l5"
    "ALD0BAgAwKqUZ3xNRNxtzPKM9885nzSFpgHAyjCEAQBYhfKM3xwjPCjlGR9eyzMKDwCggx4IAMBSSintGBEviIjHjLH61yLikJzz"
    "96bQNABYSXogAABLJ6V0zYj46hjhQSnP+NyIuIHwAABGowcCALBU5Rkj4vE1BBi1wsJxZZJFFRYAYDwCBABgmcozvjkibjrG6qU8"
    "42NyzqdNoWkAsCUIEACAZSjPeEhEvHrM8owPzDn/25SaBwBbhgABAFhYKaU9a3nGu4+x+kci4n4qLADAZJhEEQBYSCmlP4uIo8YI"
    "D3rlGf9SeAAAk6MHAgCwauUZy0SJ351C0wBgS9MDAQBYlfKMz4uIGwoPAGA69EAAABalPOPjannGHcYoz3hYzvlzU2oeACBAAADm"
    "LaV02Yh4y5jlGd8YEY9WnhEApk8PBACYsJTSlSPi4pvczDk55y/H6pdnvFctz7j7GOUZH5Rzft+UmgcADBAgAMDkvSEibrTJbZTu"
    "+AfHilKeEQCWj0kUAWCCUkrlb2uZCHCzVnY8/ybKM56lPCMAzI8eCAAwWftGxK59t0+PiCPH2M5HYjXLMz4/Ih47xurKMwLAnAkQ"
    "AGCyDhy4/Ymc8+23+k6u5RnfFhFXH6M84wsi4tk553Om1DwAYAgCBACYrIMGbpeu+lt9SEcpz/g85RkBYLkJEABguj0Qjtri5Rnf"
    "HBE3G7M842NyzqdOoWkAwBgECAAwWQcM3P7mVtzBKaVSnvEflGcEgNUhQACACUkpXSYi9u67q4zZP2Yr7eBanrEEB/cYc+LI++Wc"
    "T5pC0wCATVLGEQCmN//B0Tnn87bKDk4p3aL2uLjHGOUZHxERfyk8AIDFpQcCAEzOlpz/YJPlGb8eEYfmnI+eQtMAgAnSAwEAJmfL"
    "BQgppWtExFfGCA8uqKHDDYQHALAc9EAAgOkNYVjZCRSVZwSArUeAAAATkFIqkydeeuDu3VJKB4+wma/nnM9Y8fKMb4qIRyvPyBx9"
    "Z537DaMB6CBAAIDpDF8o3jXC+udHxB4rXJ7x1xHxwJzz+6bUNBjW9yPi/RFxx7773ti27S/sQoCNmQMBACZjrQBhFN/IOf8uFrg8"
    "Y0rpHRHx9jHCg/+KiP2FByyCtm1zRNw9Ih4UEa+NiPuWcGve7QJYBinn8hkKAGzqD2pK/1q/lPQcExG/HGETH8g5v3iByzO+eY0h"
    "GsOUZ3xiRLw6O+EAgKUnQACASfxBTel7EXHlvrtunHP+7AqUZ3xeRDxujNWVZwSAFSNAAIDN/jFNadeIOKVvaGDp3rd7zvm0JS/P"
    "+LYy9GCM8owviohn5pzPmVLzAIA5MIkiAGzeAQPzCv1gWcODWp7xsRHx/IjYYcTVj4+Iw5a95wUAsDYBAgBMfgLFI5Zxp6aULlPn"
    "Orj5GKsrzwgAK06AAACbt/QBwibLMz4o5/zeKTUNAFgQAgQAmHyAcOSy7NRSnrFUSYiIe46xeinPeL+c84lTaBoAsGBMoggAm/lD"
    "mlKZJ+B3EbF939375Jx/tug7VnlGAGAUeiAAwOZcfSA8+PmihwcppYvU8oyPH2P1MjzjkJzz0VNoGgCwwPpnjAYAVnz+g5RSKcv4"
    "lTHCg1Ka8gURcX3hAQBsTXogAMDmHLQM8x8ozwi/r2maMvxo34j4Xtu259k/AN30QACAFe+BUMszfjwi/i4iypemUZSyjtfMOX92"
    "Ss2DmWua5g4RcXJEfCsiftk0zS0cBoBuJlEEgM1d1T81Inbpu/sqOedjFmWnppTuWcsz7jHiqsozspKaptktIn41EKadEhF/1Lbt"
    "uXNsGsDC0wMBAMZ35YHwoFRj+P4i7NCU0h4ppX+JiH8ZIzwo5Rn3zzm/d0rNg3m6/ho9cXaPiAPm1B6ApSFAAIDJzX/wzZzzBfPe"
    "oSmlm5e2RETpfTCKsyLikRFxm5zziVNqHszbziPeD0BlEkUAGN+uEfG5vtsfXJDyjI8rN0dcvczdcGjO+TtTah4AsOQECAAwppzz"
    "6yKi/CxKeca3l6EHY5RnfGFEPDPnfM6UmgcArAABAgAs/0SOj4mIF4xRYeGEiDgs5/yZKTUPAFghAgQAWFK1POObImKcEnSlPOOj"
    "cs6ligQAQCcBAgAsoZTSPSLiNWOWZ3xwzvk9U2oaALCiBAgAsERKecaIeHVE3GuM1T8aEfdVYQEAGIcyjgCwJPrKM95rjPKMj1Ke"
    "EQDYDD0QAGDB1fKMz42Ix49RnvHIiDhEeUYAYLP0QACABVbLM345Ip4wYnjQK894PeEBADAJeiAAwAJSnhEAWDQCBABYrfKMb6nl"
    "GU+ZQtMAgC1MgAAAC0R5RgBgUQkQAGD5yzN+LCIOV54RAJgmkygCwHKXZ3x0RNxaeAAATJseCAAwJ8ozAgDLRA8EAFi+8owvUp4R"
    "AJg1PRAAYPblGcuwgxdExEVGXP2EiLh3zvnTU2oeAMC6BAgAMCMppUvX8ox/NsbqyjPCimia5sZjBIg9n2vb9swJNwlgKAIEAFjs"
    "8oy/iYgH55zfPaWmATPUNM3OEfE/EbHtGKufHxG7TaFZAEMRIADA9Msz/n1EHDJmecb75px/OoWmAfNxzTHDg+K7eh8A8yRAAIAp"
    "SSndrA49uMyIq55dLlSW4CHnfMGUmgfMx0EDtz9ZexYMoywLMDcCBACYTnnG54xRYaE4MiIOzTl/24GBlXStvv//om3bm8+xLQAj"
    "ESAAwASllK4eEW+r3ZRjxPKMbUQ8Ped8joMCW6IHwpfm2A6AkQkQAGAClGcEujRNU3on7dd3lwABWCoCBACYb3nGt0bEI3POpzgQ"
    "sPKuERHb990WIABLRYAAAJuQUrp7RLxWeUZgxOELZdjSV+w1YJkIEABgDCml3Wt5xkPHWF15Rpif9Xr7nDLjAOF7bdvqeQQsFQEC"
    "AIwopXTTWp7xsmOUZ3xSRLxKeUaYmy/WsKCEgD0nRsQ3Z1yB4WdN09xyiHXOb9v2f6bYJoChpZxL7ykAoPOPpvKMsBKaprleRLw5"
    "Iq4SEUdFxL3atv3WlB+zzH1wWkSUiRRH8e22bUt1F4C50wMBAGZTnvEZOefSAwGYs7Zty+SFV22aZue2bc+Y0cP+6RjhQfH1KbQF"
    "YCwCBADoLs/4qIh44Rgn/z+KiMNyzp+2k2HxzDA8GBy+cEFEDDss4T+n1B6AkQkQAGAdyjMCE9Q/geIxbdsOM/8BwEIRIADAGlJK"
    "d6vlGfcccQf9JiIeknN+lx0LrBMgHGnPAMtIgAAAkyvP+PGIODzn/FM7FehpmmbbiLhG3x4RIABLqYzrBAD+f3nGb44RHpTJER8T"
    "EX8hPADWcLWI2LnvtgABWEp6IACw5dXyjM+OiCeWHGHEHfKNiDgk5/ztLb8jgWGGL2w6QGia5mZ1iFWp8nL9tm1P2WDZ10XETSLi"
    "A23bPskhAjZDDwQAtrSUUimtVkq6NSOGB73yjNcTHgAjBAg/a9v255vcY0dHxFVKKcqIuM56CzVNc/OIeGBEXDYiXuMoAZslQABg"
    "y5ZnTCk9OiK+FhHXHKM8481zzk/KOZfhCwDDlnDc9PCFGkD8sN683gbzLryi3nxR27bHO0TAZgkQANhyUkp/HBH/FREvj4gyfGEU"
    "byuToeWcPzWl5gErpGmaNBBSTmr+g8/Xf6+7zu8fFhH7R8RxJUCY0GMCW5wAAYCtWJ7xqIi45RjlGe+ecz4s57zueGOAAVeOiN2m"
    "GCD8QQ+Epmn2iohn1ZuPbdv2LEcFmASTKAKwJSjPCPQ0TVPKtT45Ig6sc6CULv5nzGD4wjQChEs0TXPZtm3L0Kqe50XEnqWnVdu2"
    "H5jQ4wEIEABYfSmlMgP5W+tEYqM4u37JeGXO+YIpNQ+YoaZpSg/cj5TqBfWuv6jDAG4zgwkUT4+IYye03dKT6rTau6H0QrgwQGia"
    "5oA6ceI5EfGoCT0WwIUMYQBgpcszppTK2N9PjhEelPKM1845v1x4ACvl6n3hQc+ty1X8GQQIR7VtO5Ewsm6n9J4YnAfhlfUc/2Vt"
    "2x4ziccC6BEgALCSNlme8cW1POO3pthEYD6uMOL9m3VyRPx3/XnPhLf9e/MgNE1zz4i4cUT8NCKeM+HHAjCEAYDVK88YEY+ss46P"
    "WmGhdAG+twoLwKS0bXvXKe7NL9R/D2qa5qLl4ertJ7RtW4ZLAEyUSRQBWLXyjG+MiFuNsXopz/gIFRaAJVIChDKUYZf6GXbpMmSr"
    "bdt/nXfDgNVkCAMAKyGldNc6qdio4cFvI+IeyjMCy6Zt21JS9uh683YRcV7tgQUwFQIEAJa+PGNK6S0R8a5atmwUZUzy/jnnd06p"
    "eQDT1psHoXh127bmbgGmRoAAwLKXZyzVEg4bozzj4yLiz3POP5lS8wBm4bv1319ExDPscmCazIEAwNJJKe0QEc8eo8JC8c2IOESF"
    "BWDZNU2zbUQ8sN58Uh3SADA1AgQAlrE8Y5ks7IARVy3lGf8uIp6Wcy49EACW3d9ExFXrMIY3z7sxwOoTIACwTOUZH1HLlI1anvHH"
    "tTzjJ6fUPICZaZqm9Ly6f0Q8MyLOiYiHtG1bQlKAqRIgALDq5RnfXsszlmoLAEuraZpHR8RDI+LifZPGPrZt21KBBmDqBAgALEN5"
    "xn8co8JCCQweosICsEJuERFXqf8/MSKe27bta+bcJmALESAAsLDlGSPilWXowRirfyIi7qPCArBiHlUnjy0B6S8MWwBmTYAAwMJJ"
    "Kd04It4aEZcbcdWz66Rir8g5XzCl5gHMRdu2J9j1wDwJEABYGMozAgAsLgECAAshpbRfnfBQeUYAgAUkQABgUcozvigidhxxdeUZ"
    "AQBmRIAAwNyklC4VEW9SnhEAYPGVqz4AMHMppbtERKldfqsRVy2zj98z53xozrn8HwCAGdADAYBlK894eM65DF0AAGCG9EAAYNbl"
    "Gb8xRnhQyjM+rvRWEB4AAMyHHggAzKo847Mi4knl5oirl2EOh+Scy78AAMyJAAGAWZRnfFtEHDjiqjkiXhIRT805lx4IAADMkQAB"
    "gGmWZ3x4RLRjlme8T875fxweAIDFIEAAYFrlGd8YEX8+xur/UoIHFRYAABaLSRQBmFZ5xj8fszxjme9AeUYAgAWjBwIAE5FSumgt"
    "z3ifMVZXnhEAYMHpgQDAJMszjhoenBMRj1eeEQBg8emBAMDYlGcEllAe8X4AKgECAPMoz/jSWp7xLLsfmLEj17jvgoj4piMBsDFD"
    "GAAYSfpfj4yIr40RHpTyjH+Wc36C8ACYh7ZtfxQRrx24+4Vt25q8FaCDHggADE15RmBFPDwiPhgRB0XElyLiv+fdIIBlkHI23AuA"
    "If5gpHTniHhdRFxsxP11SkQ8NOf8DvsZAGB56YEAwDTLM/5PWS/nXIYuAACwxMyBAMC0yjM+ISJuKTwAAFgNeiAAsF55xmdGxJPL"
    "zRF30VERcWjO2YzmAAArRIAAwO9JKV2tlmcsk4uN6iXKMwIArCYBAgAXKrUZ68zkL46IHUfcLT+pcx18wu4EAFhNAgQAeuUZ3xAR"
    "fzHG7ijVFR6ec/6NXQkAsLoECABb3CbLMz4s5/wvU2oaAAALRIAAsLXLM74iIg4fszzj4TnnH02haQAALCBlHAG2oJTSwbU84+Gb"
    "KM8oPAAA2EL0QADYeuUZn1HLM44aIn8rIg5RnhFYBU3TXCIiDoiIr7Vt+6t5twdgGeiBALC1yjN+ISL+dozP/5dGxHWEB8AqaJrm"
    "QRHxs4j4SPm3aZq7z7tNAMsg5Zzn3QYApkh5RoD/r2mavSLil+Xjse/usyJiz7Zty78ArEMPBIAVllLaJyI+FBGviogdxyjPeI2c"
    "8yem1DyAebjuQHgQ9fPxQIcDYGPmQABYUSmlO9XyjOVq2yiUZwRW2Q4j3g9AJUAAWDGbLM/4yYi4jwoLAAAMMoQBYIWklG4UEUdu"
    "ojzjnwkPAABYix4IACtAeUYAAKZNgACw5FJKV42It0fEQWOsXsozPiXnbOZxAAA2JEAAWO7yjA+LiBdHxE4jrv7TOtfBf0+peQAA"
    "rBgBAsDylmd8Q0TceozV/7UEDznn30yhaQAArCgBAsCSSSn9dUT8k/KMAADMkgABYEmklHar5RnvO8bqyjMCALApyjgCLE95xm+M"
    "ER6U8oxPVJ4RAIDN0gMBYIGllLaPiGdExN+MEfp+OyIOyTmX4AEAADZFgACw2OUZ3xYR1xpj9ZdFxN8qzwgAwKQIEAAWjPKMAAAs"
    "IgECwOqUZ3xnLc/46yk0DQCALc4kigCLVZ7xqDHCg1Mi4tCIuKfwAACAadEDAWC5yzN+KiLunXP+0RSaBgAA/0cPBIA5SindMCKO"
    "HCM8ODciGuUZAQCYFT0QAOZAeUYAAJaNAAFgucozvjwi/kZ5RgAAZk2AADDb8owPjYi/i4idRlz9pxFxeM7541NqHgAAbEiAADAD"
    "KaVL1vKMtxlj9XeV4EGFBQAA5skkigCzKc/4rTHCg1Mj4rCIuIfwAACAedMDAWC65RnLnAX3G7M8431yzidMoWkAADAyPRAAplue"
    "8X6bKM8oPAAAYGHogQAw+fKMT4+Ivx0jpP12RByacy7BAwAALBQBAsCEpJSuUsszXnuM1ZVnBABgoQkQADZJeUYAALYCAQLAJijP"
    "CLB0frXO/b+ccTsAlo5JFAHGlFK6Y0QcpTwjwFL5ckT8dOC+70bE0XNqD8DSECAAjFGeMaX0+oj4t4jYe4zyjNfIOb8t55ztfIDZ"
    "atu2VLu5RUR8PCJ+HREfiog/b9vWZzJAh+T8FWB4KaUb1IkS/2TE/VZOWJ8aES/JOZ9vnwMAsGzMgQAwBOUZAQDY6gQIANMtz/iK"
    "iPibnPOZdjQAAMtMgACwcXnGh5RhBxGx04g76sSIODzn/DE7GACAVSBAAFi/POM/R8RfjrGD3hURD805l8m5AABgJajCADAgpXSH"
    "Wp5x1PDg1Ig4LCLuITwAAGDV6IEA0FeeMSJeFhH3H2OnfDoi7p1zPsEOBQBgFemBAPD/yzMeOUZ4UMozPqnUFBceAACwyvRAALa0"
    "Wp7xaRHxlDFC1e9ExKE55yOm1DwAAFgYAgRgy0opXbmWZ7zOGKsrzwgAwJYiQAC2annGB0fES5VnBACA4QgQgK1YnvH1EXHbMVZ/"
    "d0Q8RIUFgOXWNM2lIqKNiAMj4ksR8cS2bU+ed7sAFl3KOc+7DQCzLM9YwoO9R1z1tIh4eBnukH1oAiy1pmm2jYhvR8RV+u7+ckRc"
    "v21bJ8YAG1CFAVh5KaVdU0olOHj/GOHBZyLiGjnntwoPAFbCQQPhQXHdiLjSnNoDsDQECMBK22R5xidHxM1zzsdPqXkAzN6lRrwf"
    "gMocCMBKUp4RAAAmS4AArJxNlmd8Zel5kHM+cwpNAwCApSVAAFaxPONLImLnEVc/MSIOzzl/bErNAwCApSZAAFZCSukSEfHPY5Zn"
    "fE8tz6iEFwAArMMkisDSSyndPiKOGiM8KOUZ7xMRdxMeAADAxvRAAJa6PGNEvCwiHjDG6qU8471VWAAAgOHogQAse3nGB4xRnvFv"
    "lGcEAIDR6IEALGN5xqfWn1FD0KMj4pCc8xFTah4AAKwsAQKwNJRnBACA+REgAMtSnvFBEfHSMcoznlTLM350Ss0DAIAtQYAALEN5"
    "xtdHxF+NsbryjAAAMCEmUQSWoTzjqOGB8owAADBheiAAi1qesQxXeOAYq382Ig5TnhEAACZLDwRgoaSUrh8RR4wRHvTKM95MeAAA"
    "AJOnBwKwSOUZn1LLM2474urKMwIAwJQJEIC5SyntGxFvi4jrjrH6qyLiSTnnM6fQNAAAoBIgAMtcnvG+Oef/mlLzAACAPgIEYBnL"
    "M743Ih6ccz55Ck0DAADWYBJFYOZSSrcbszxj8fcRcVfhAQAAzJYAAZhpecaU0usi4oMR8UdjbuYOYwx3AAAANkmAAMxESul6Y5Zn"
    "zAO3L1PLNQIAADMkQACmXp4xpfTMiPhcRFxpjPKMt4mI0wfuf2JKadRtzV1KaZuU0rVTSndOKd0vpfQXKaVLzrtdAAAwDAECMO3y"
    "jJ+NiGdExLZjlGe8Vq2y8JyB3+0QES+L5Rq68byI+HFEfCUi3hMR/xwRHyn3pZTekVK6+LzbCQAAGxEgAFMpz5hSKuUZj4yI645R"
    "nvHWOedH5ZzPrPe9PCKOHVjur1JK40zCOFMppZtGxLci4m8j4lLrVMO5R0R8IaV02Tk0EQAAhiJAACaqXkkvkyT+4xiTHZbyjPvX"
    "Xgf/J+d8dkQ8ao3lX55S2jEWVBmiUHsZXK7edVR9HreMiDtHxLv6Fv+Tus8AAGAhCRCASZdnLFfbR+0ZcFpEHL5Recac80dqMNHv"
    "ihHxmFhAKaXS8+L9EdELOMoQhgNyzq/KOf93zvl9Oee7R8Sz+1a7dUrpz+bUZAAA2JAAAZjUGP9/HLM8Y5lc8Zo55zfnnAcrLgx6"
    "bESU3giDEyruFgu2PyLi7X3hwYtzzk/NOV+wxuJlfocT+m7fbUbNBNiqzl/n/vNm3A6ApSNAACZVnrHMeTCK8+q8ADfNOR83zAo5"
    "5x+WL+MDd18sIh4Wi+X5fRUnjtio7GTO+bw6qWLPraffPIAtrUxmO+jcOm8PABsQIABjSSltt4nyjN+NiOvnnF+Qc17vStB6XhIR"
    "pw7c94SU0i6xAFJKl4mIB/fd9YQhnuN3+v5/6VL6ckrNA9jy2rb9eUQ8bWBHPK5t28GSwQAMECAAsy7P+Pe1POPXxtn1OeffRsQr"
    "Bu7eOyIeEovhb2uZyeJrOedPDLFOeU79n8uXnlLbAIgoIcJzI+Iadf6dq7VtW/42AdAhdQ85BqgfGCmliHhgRLxsjAoLPysnaoMV"
    "FsaRUrpYnTegzDXQU64o/UnO+Yx5Ha+U0s61Hb12PTTn/Noh1rtLRLy7764r5Zx/ML2WAgDA6PRAAEYpz/iBMcszvm+t8ozjyjn/"
    "OiJeNXD3JWq4MU936AsPynjadw65Xq/HQs9ZE24XAABsmgAB6JRSKmUZj4qIUqZxFL+LiPtGxF1yzr+a8K5+aUQMjld9UkqpV/lg"
    "HkpZxp7P5Jx/M+R6pUfF4H4DAICFst28GwAsrjox4UvHqLAQdXLFe9fKCRNXAomU0qsjoum7e5+IuGtEvDVmLKVUAtmb9d11fEqp"
    "//ZGDuz7/69zzqdMuHkAALBp5kAANirP+LYxKiycVydXfNEYFRbGGVZR5kLo73XwuZzzwdN83HXaUkKAr09gU1/KOV9/AtsBAICJ"
    "MoQBWKs84zM2WZ7x+dMOD4qc8y8i4l0Dd98opfSnMXs3mtB2vjeh7QAAwEQZwgAMlmcs3f9L74NRXTicYA5VEMqkjvceuO/BEfGo"
    "Gbdjv4GyjMOWqdw+Im7Sd/vzE24XAABMhCEMQK884wMi4uVjlme8b875I3Ns+zcj4uoDX+D/eJZhRkrpYxFxy3rzfTnnOw+53s0j"
    "4hN9d+2Xcz56Oq0EAIDxGcIAW1ydR+D9EfG6TZRnnEt4UOScc+2F0G+POpniLF2x7/8/GmG9XuhQ/EJ4AADAohIgwBbWV57x9gtU"
    "nnEcZbLHM9cYxjBLu/f9/+cjrHfbvv+/Z4LtAQCAiTIHAmzd8owvGfNL9lTLM44j5/zblNI7I+LwvrtvUCZTzDl/e0bN2HEgYOmU"
    "UrpqRFxzIAgBYMqapinD3w6sP19u27aE6QB00AMBtpiU0nUj4ogxwoNSnvEpEXHTRQoP+gwOY4gZD2MoJ6M9w1aguH/f/7+bc/7C"
    "hNsEwNqeWSe7fX2ZR6dpmsfYUQDdBAiwtcozPr3O8l+qLYxaWnBm5RnH9KWI+P7AfXeZ4eOf2Pf/i3YtnFIqyzyo765nTadZAPRr"
    "muaSEVH+HvZrm6bZ1Z4C2JgAAbaAlNKVIuIz9UvqtmOUZzwo5zxsWcJ5TqY4OIfAn6aUrjajJhzf9/+rDHn1qxc0lK6z75pSuwD4"
    "fddep6TuAXYUwMYECLDCSonDlNIDI+LI0oNgjPKMt8k5P2KW5RA36d1r3DdUOcUJ+FTf//8ipbTDegumlP4sIh5Vb55bhjLknC+Y"
    "fhMB2CBIHzVgB9hyBAiwNcozlkkTR/Fv8y7POKYyt8NxA/fdbkaP/d6+/18qIp6w1kIppRvXZXsnqk/POX9lNk0EAIDxCRBgBaWU"
    "bruJ8oz3K1ftF6Q84zjDGD44cPd1U0qXnMFjf2dgCMVzU0ovKZUWUkp7ppSulVJ6VUR8oq/k46tzzi+cdtsAAGASBAiwYuUZU0qv"
    "jYj/iIjSA2EUZXLFa+ac31i/iC+rwQChKIHKLJRZvH/aV5XhcRFxdET8OiK+GhGPqOVzy3CFF5XhITNqFwAAbJoAAVbEJsszPnWB"
    "yzOOqkwWecrAfbeZxQPnnEt4cIMaxqznq3VfP3kWbQIAgEkpV8KAJS/PGBF/W0tSbTtGecZDc87lS+1KyDmfm1L62EAJx4PLbJKz"
    "6FmRc/5xRNwopXS9EhRExGUj4uyI+FFEfDzn/O1ptwEAAKZBgADLX57xrWNUWOiVZ2yWqMLCKD49ECBcIiKuGBHfn1UDcs5fiojy"
    "AwAAK8EQBlje8owP2ER5xr9csvKMo/rsGvfdaA7tAACAlSFAgCWTUvqjWp7xn8Yoz/j+Wp7xw7HajqoVJfodPKe2AADAShAgwNYp"
    "z3j/iLjTMpZnHFXOuUwM+YWBuwUIAACwCQIEWJ7yjK+p5RnLeP5xyjO+YcnLM252GMNVU0p7z6ktAACw9AQIsOBSStep5RkfssXL"
    "M05iHoQbzqEdAACwEgQIsKBKecaU0tNqV/x9xyjPeIOc8/Nqd/6tqFRAOH/gvlJaEQAAGIMAARZQSqmUHPxMRDw7IrYdcfV/iIiD"
    "cs5fjS0s53x6RBw9cPdV59QcAABYegIEWMzyjN8YozzjzyPitjnnh69wecZRfXfg9lXm1A4AAFh62827AcDvlWcspRnvMMY+KeUZ"
    "H5Rz/qX9+QdDOfrtm1LaNuc8OLQBAADooAcCLICU0l/W8ox32ER5RuFBd4CwQ0RcfhOHCgAAtiwBAixGecb/HKM8Y5lc8YAtWJ5x"
    "M0MYCvMgAADAGAQIMN/yjF8fszxjqc5wk5zzD6bUvFXtgVCYBwEAAMYgQID5lWf8fERcecTVj4mIG+acn7uFyzMOLed8akScNHC3"
    "AAEAAMYgQIDZl2f8dC3POOokpq+p5Rm/MqXmbZVeCFeaUzsAAGCpqcIAM1BqM0bE/SLiFRGxyxjlGe+Xc/7QlJq36n46cLtUuwAA"
    "AEYkQIDZlGd8XUTccYzVPxARD1RhYVN+NXB7r81tDoBpaJrmpRHx2HqzDNO7dNu2JUQHYEEYwgCzKc84anhwekQ8ICL+Wngw8QBh"
    "79ojBIAF0TTNQ/vCg95Frp81TfN3TdOMWqUIgCkRIMAUpJR2Tin9wybKM14z5/zPyjNOxMkDt3eIiF0ns2kAJqT8zVzL4yPiOEEC"
    "wGIQIMB0yjMeERHlasoozleecSY9EArDGACWx06CBIDFIECACUop3SoiPjdmecYbKM84kx4Ixd7TeSgAxlQqFHURJADMmQABJiSl"
    "9McR8b6I2H7EVZVnnC49EAAW349GWHazQcJgdZ6en4y4HYAtR4AAk3O7EcfWl5mlb5tzfljOuUyayOx6IBjCALD8xg0SyjDD7wzc"
    "98W2bX8whTYCrJSUc553G2AlpJReFhGPGWbZHXbY4aM3vvGNn3zQQQf9esLNOK1t27G32TTNjmNM+rgZ5QPoJ23bXjDOyk3TlGoK"
    "l6wTI67p6KOP3uPTn/70kf337bnnno+/293u9t5xHjMiftO27aljrlvavMuMh1CUuTV+2rZt3sQ+Lr1rto3Z+VXbtmOHak3T7B4R"
    "e8TsnN227c/GXblpmhLmX7p8jMTs/Kxt27PHXblpmotFxG4xO2e0bfvLcVdumqb0DLtUzFZ535VShGNpmqaUAN45Zmfefz/K39C/"
    "js05s07G+OKu8o9N05S/Hc+PiIMi4ksR8eS2bX+zyccHWHkCBJjUmymlh9ThCOvafvvt4xa3uEXsv//+Zflp7fsvRsRd27Yduitm"
    "0zTly+GrIuLwekVn1j0EntK27T+OslLTNDeNiDdGxBVitkrY8bGIuEfbtr8ddqWmacp+fXMt6TnqMJfNOjEiHtm2bRliM7Smae4S"
    "Ea+MiH1its6NiBLw3Ldt27OGXalpmj0j4p0R8Wdz6GH3w4i4T9u2nx1lpaZpHhYRz55Dr5jyResNEfHotm1LyDSUpmkuGxHvjojr"
    "xux9q77vvj1iAPbMWh5wloFHUYLGl0TEc0YJ8JqmuXp9He8Xs7dsfz82en3fu23b98y7IQCrRoDAUrj2ta9drmxcMRbYySeffLHj"
    "jz/+/RFRrsz9gX322Sdue9vblqvfU2/Leeedd8SnP/3pw4Zd/rrXve59dt111yfGHJ100kn3Ovroo785zLJ77LHHLgceeOAnU0pz"
    "O1k955xzPvzZz3526H12wxve8Ek77rjj0Mdk0nLO5/3gBz/4yx/96EclTOh0+ctf/jJXuMIV/iOlNMueB7/nzDPPfNMXvvCFvxt2"
    "+YMPPvhlO+ywQ5nIdC5yzmd89atfvelpp51Wvrx02m+//Q685CUv+daYo9/97ncv/PKXv/y2YZe/6U1v+o5tt912/5iTCy644KRP"
    "fepTtxq29+SBBx546z333HPo19A0/PrXv37skUceWULHTttss026yU1u8rFtttmmXB2fi2X8+7GWUgb5+OOPv+1xxx03ytwKwOT9"
    "4Ktf/erQFwNYfNvNuwEwpCvWq08La6+99rqwh8Fxxx1XTsD+7/5tttkmbnCDG8T1r3/9C/8/C9tuu+2B22yzzbcuuGC4kQFnn312"
    "7LrrKNM3TN4ZZ5zxL8MuW3pvTLEHx7BuU3+G0v+amIeU0nbnnHPOR4ddvrwm5r2PzzvvvHJFs/wMZd7tTSntvO22235l2OXPOOOM"
    "mLezzjrryaXr9jDLbrvtthf+zNM222yzz4477vitM888c+h9PIvQtqMNpWv+UHbccceZ/Z1Ypb8fa0kppbPPPvtD824HEKVX1dA9"
    "x1h8AgSYoIte9KIXDk8o/5YT15122imufvWrxy67lGHvs1NO6IY9+StKW0sAMk+jfJlahC9eo7ahLD/vk+zTTz99Kssu0j7effcy"
    "/cH8LNvreJTjfP7551/42XKRi1xkqm0apg3LtI9HacNZZ5114Wf3PEOEZfz7scifYwCrRhUGmPSbapttLvwSc7Ob3Syud73rzTw8"
    "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"
    "JEAAAAAAOgkQAAAAgE4CBAAAAKCTAAEAAADoJEAAAAAAOgkQAAAAgE4CBAAAAKCTAAEAAADoJEAAAAAAOgkQAAAAgE4CBAAAAKCT"
    "AAEAAADoJEAAAAAAOgkQAAAAgE4CBAAAAKCTAAEAAADoJEAAAAAAOgkQAAAAgE4CBAAAAKCTAAEAAADoJEAAAAAAOgkQAAAAgE4C"
    "BAAAAKCTAAEAAADoJEAAAAAAOgkQAAAAgE4CBAAAAKCTAAEAAADoJEAAAAAAOgkQAAAAgE4CBAAAAKCTAAEAAADoJEAAAAAAOgkQ"
    "AAAAgE4CBAAAAKCTAAEAAADoJEAAAAAAOgkQAAAAgE4CBAAAAKCTAAEAAADoJEAAAAAAOgkQAAAAgE4CBAAAAKCTAAEAAADoJEAA"
    "AAAAOgkQAAAAgE4CBAAAAECAAAAAAGyeHggAAABAJwECAAAA0EmAAAAAAHQSIAAAAACdBAgAAABAJwECAAAA0EmAAAAAAHQSIAAA"
    "AACdBAgAAABAJwECAAAA0EmAAAAAAHQSIAAAAACdBAgAAABAJwECAAAA0EmAAAAAAHQSIAAAAACdBAgAAABAJwECAAAA0EmAAAAA"
    "AHQSIAAAAACdBAgAAABAJwECAAAA0EmAAAAAAHQSIAAAAACdBAgAAABAJwECAAAAEF3+H0k3mklV84ffAAAAAElFTkSuQmCC"
)

_NOTES = """
## Components of Vectors — Resolving Forces

**Definitions:**
- A vector can be resolved into two components at right angles to each other — usually
  horizontal and vertical, or parallel and perpendicular to a slope.
- Resolving a vector does not change it; the two components together are exactly
  equivalent to the original vector.

$$F_x = F\\cos\\theta \\qquad F_y = F\\sin\\theta$$

For an object of mass m on a slope inclined at angle θ to the horizontal, with weight
$W = mg$:
$$W_{\\parallel} = W\\sin\\theta \\ \\text{(component down the slope)} \\qquad W_{\\perp} = W\\cos\\theta \\ \\text{(component into the slope)}$$

If the object is sliding **down** the slope, friction acts up the slope, opposing the
motion, so the resultant force down the slope is $W_{\\parallel} - \\text{friction}$. If
the object is sliding **up** the slope (e.g. after being pushed), friction still opposes
the motion — so it now acts down the slope, in the same direction as $W_{\\parallel}$ —
and the two add together: resultant $= W_{\\parallel} + \\text{friction}$, decelerating
the object.

| Symbol | Quantity | Unit |
|---|---|---|
| F | Size of the force (or W = weight) | N |
| θ | Angle to the horizontal (or to the slope) | ° |
| Fx, W∥ | Component parallel to the reference direction | N |
| Fy, W⊥ | Component perpendicular to the reference direction | N |

**Worked Example:** A force of 50 N acts at 40° above the horizontal. Resolve it into
horizontal and vertical components.
$$F_x = 50\\cos40° = 38.3\\ \\mathrm{N} \\qquad F_y = 50\\sin40° = 32.1\\ \\mathrm{N}$$

![Resolving a force into components](data:image/png;base64,%%COMPONENTS_DIAGRAM%%)

> **Important:** Always check which angle is given — the angle to the horizontal, or the
> angle to the slope/vertical — since this decides whether a component uses sin or cos.
"""

_NOTES = _NOTES.replace("%%COMPONENTS_DIAGRAM%%", _COMPONENTS_DIAGRAM_B64)

_ANGLES = [20, 25, 30, 35, 40, 50, 55, 60, 65, 70]
_OBJ = ["crate", "box", "sledge", "block", "barrel", "trunk"]


def _r1(val):
    return round(float(val), 1)


def _obj():
    return random.choice(_OBJ)


# ── Level 1 — Finding Components ─────────────────────────────────────────────

def gen_rf_l1_components(level="Higher"):
    F = random.randint(20, 200)
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)

    Fx = _r1(F * math.cos(theta))
    Fy = _r1(F * math.sin(theta))
    Fx_swap = _r1(F * math.sin(theta))
    Fy_swap = _r1(F * math.cos(theta))

    context = (
        f"A force of F = {F} N acts at an angle of {theta_deg}° above the horizontal."
    )

    working_x = [
        {"type": "text",  "content": "The horizontal component uses cos θ:"},
        {"type": "latex", "content": r"F_x = F\cos\theta"},
        {"type": "latex", "content": rf"F_x = {F} \times \cos {theta_deg}° = {Fx}\ \mathrm{{N}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the horizontal component of the force.",
        correct_answer=Fx, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_x,
        distractors=[
            {"value": Fx_swap,
             "mistake": f"The horizontal component uses cos θ, not sin θ. Fx = F cos {theta_deg}° = {Fx} N.",
             "working": working_x},
            {"value": float(F),
             "mistake": "This is the full force. Resolve it using Fx = F cos θ.",
             "working": working_x},
        ],
        notes=_NOTES,
        scaffold=[
            {"prompt": f"What is cos {theta_deg}°, to 3 decimal places?", "answer": round(math.cos(theta), 3)},
            {"prompt": "What is the horizontal component Fx?", "answer": Fx},
        ],
    )

    working_y = [
        {"type": "text",  "content": "The vertical component uses sin θ:"},
        {"type": "latex", "content": r"F_y = F\sin\theta"},
        {"type": "latex", "content": rf"F_y = {F} \times \sin {theta_deg}° = {Fy}\ \mathrm{{N}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the vertical component of the force.",
        correct_answer=Fy, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_y,
        distractors=[
            {"value": Fy_swap,
             "mistake": f"The vertical component uses sin θ, not cos θ. Fy = F sin {theta_deg}° = {Fy} N.",
             "working": working_y},
            {"value": float(F),
             "mistake": "This is the full force. Resolve it using Fy = F sin θ.",
             "working": working_y},
        ],
        notes=_NOTES,
        scaffold=[
            {"prompt": f"What is sin {theta_deg}°, to 3 decimal places?", "answer": round(math.sin(theta), 3)},
            {"prompt": "What is the vertical component Fy?", "answer": Fy},
        ],
    )

    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    )


# ── Level 2 — Components of a Balancing Force ────────────────────────────────

def gen_rf_l2_balancing(level="Higher"):
    Fx_known = random.randint(80, 300)
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)

    T = _r1(Fx_known / math.cos(theta))
    Ty = _r1(T * math.sin(theta))

    context = (
        f"An object is held in equilibrium by two ropes. Rope A pulls horizontally with a "
        f"force of {Fx_known} N. Rope B is inclined at {theta_deg}° to the horizontal, and "
        f"its horizontal component exactly balances the pull of Rope A."
    )

    working_T = [
        {"type": "text",  "content": "Since the ropes balance, the horizontal component of Rope B's tension equals Rope A's pull:"},
        {"type": "latex", "content": r"F_x = T\cos\theta \;\Rightarrow\; T = \dfrac{F_x}{\cos\theta}"},
        {"type": "latex", "content": rf"T = \dfrac{{{Fx_known}}}{{\cos {theta_deg}°}} = {T}\ \mathrm{{N}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the tension in Rope B.",
        correct_answer=T, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_T,
        distractors=[
            {"value": _r1(Fx_known * math.cos(theta)),
             "mistake": f"You multiplied by cos θ instead of dividing. Rearranging Fx = T cos θ gives T = Fx ÷ cos θ = {T} N.",
             "working": working_T},
            {"value": float(Fx_known),
             "mistake": f"The tension in Rope B is not equal to Rope A's pull — only its horizontal *component* is. T = {Fx_known} ÷ cos {theta_deg}° = {T} N.",
             "working": working_T},
        ],
        notes=_NOTES,
        scaffold=[
            {"prompt": f"What is cos {theta_deg}°, to 3 decimal places?", "answer": round(math.cos(theta), 3)},
            {"prompt": "What is the tension T in Rope B?", "answer": T},
        ],
    )

    working_Ty = [
        {"type": "text",  "content": "Now find the vertical component of this tension:"},
        {"type": "latex", "content": r"F_y = T\sin\theta"},
        {"type": "latex", "content": rf"F_y = {T} \times \sin {theta_deg}° = {Ty}\ \mathrm{{N}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the vertical component of the tension in Rope B.",
        correct_answer=Ty, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_Ty,
        distractors=[
            {"value": _r1(T * math.cos(theta)),
             "mistake": f"The vertical component uses sin θ, not cos θ — and since T cos θ was already used to find T from Rope A's pull, this just gives back {Fx_known} N. Fy = T sin {theta_deg}° = {Ty} N.",
             "working": working_Ty},
            {"value": T,
             "mistake": f"That is the full tension in Rope B, not its vertical component. Fy = T sin {theta_deg}° = {Ty} N.",
             "working": working_Ty},
        ],
        notes=_NOTES,
        scaffold=[
            {"prompt": f"What is sin {theta_deg}°, to 3 decimal places?", "answer": round(math.sin(theta), 3)},
            {"prompt": "What is the vertical component of the tension?", "answer": Ty},
        ],
    )

    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    )


# ── Level 3 — Force from Acceleration ────────────────────────────────────────

def _l3_horizontal_find_F(level):
    m = random.randint(10, 60)
    a = random.choice([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
    F = _r1(m * a)

    question = (
        f"A {_obj()} of mass {m} kg accelerates at {a} m/s² across a smooth horizontal "
        f"surface when pushed. Calculate the horizontal component of the force applied."
    )
    working = [
        {"type": "text",  "content": "Apply Newton's second law:"},
        {"type": "latex", "content": r"F = ma"},
        {"type": "latex", "content": rf"F = {m} \times {a} = {F}\ \mathrm{{N}}"},
    ]
    options_data = [
        {"value": F, "mistake": None, "working": working},
        {"value": _r1(m / a),
         "mistake": "You divided instead of multiplying. F = m × a.",
         "working": working},
        {"value": _r1(m + a),
         "mistake": "Force is the *product* of mass and acceleration, not their sum. F = m × a.",
         "working": working},
    ]
    return make_question(question, F, options_data, "N",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Components of Vectors", level=level)


def _l3_horizontal_find_a(level):
    m = random.randint(50, 400)
    F = random.randint(60, 500)
    a = _r1(F / m)

    question = (
        f"A trailer of mass {m} kg is pulled across level ground by a horizontal force of "
        f"{F} N. Calculate the acceleration of the trailer."
    )
    working = [
        {"type": "text",  "content": "Rearrange Newton's second law for acceleration:"},
        {"type": "latex", "content": r"F = ma \;\Rightarrow\; a = \dfrac{F}{m}"},
        {"type": "latex", "content": rf"a = \dfrac{{{F}}}{{{m}}} = {a}\ \mathrm{{m/s^2}}"},
    ]
    options_data = [
        {"value": a, "mistake": None, "working": working},
        {"value": _r1(m / F),
         "mistake": "You divided the wrong way round. a = F ÷ m, not m ÷ F.",
         "working": working},
        {"value": float(F),
         "mistake": "This is the force, not the acceleration. a = F ÷ m.",
         "working": working},
    ]
    return make_question(question, a, options_data, "m/s²",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Components of Vectors", level=level)


def _l3_vertical_given_a(level):
    m = random.randint(5, 40)
    a = random.choice([0.3, 0.5, 0.8, 1.0, 1.2, 1.5, 2.0])
    W = _r1(m * G)
    mode = random.choice(["up", "down", "constant"])
    obj = _obj()

    if mode == "up":
        T = _r1(W + m * a)
        context = f"A {obj} of mass {m} kg is lifted vertically by a crane, accelerating upwards at {a} m/s²."
        rule_text = "Since the object accelerates upward, the tension must overcome its weight AND provide the extra force for the acceleration:"
        eq_latex = r"T = W + ma"
        sub_latex = rf"T = {W} + ({m} \times {a}) = {T}\ \mathrm{{N}}"
        wrong_T = _r1(W - m * a)
        wrong_mistake = f"Since the object accelerates upward, ma must be added to the weight, not subtracted. T = W + ma = {T} N."
    elif mode == "down":
        T = _r1(W - m * a)
        context = f"A {obj} of mass {m} kg is lowered vertically by a winch, accelerating downwards at {a} m/s² (less than g, since the cable is still under tension)."
        rule_text = "Since the object accelerates downward (more slowly than free fall), the tension must be less than the weight, but still positive:"
        eq_latex = r"T = W - ma"
        sub_latex = rf"T = {W} - ({m} \times {a}) = {T}\ \mathrm{{N}}"
        wrong_T = _r1(W + m * a)
        wrong_mistake = f"Since the object accelerates downward, ma must be subtracted from the weight, not added. T = W − ma = {T} N."
    else:
        T = W
        context = f"A {obj} of mass {m} kg is raised at a constant speed by a winch cable."
        rule_text = "At constant speed the object is in equilibrium, so the tension simply equals the weight:"
        eq_latex = r"T = W"
        sub_latex = rf"T = {W}\ \mathrm{{N}}"
        wrong_T = _r1(W * 1.1)
        wrong_mistake = f"At constant speed there is no acceleration, so the tension equals the weight exactly: T = W = {T} N."

    working_W = [
        {"type": "latex", "content": r"W = mg"},
        {"type": "latex", "content": rf"W = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the weight of the object.",
        correct_answer=W, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_W,
        distractors=[
            {"value": float(m),
             "mistake": "Weight is mass × g, not mass on its own. W = mg.",
             "working": working_W},
        ],
        notes=_NOTES,
    )

    working_T = [
        {"type": "text",  "content": rule_text},
        {"type": "latex", "content": eq_latex},
        {"type": "latex", "content": sub_latex},
    ]
    distractors_T = [
        {"value": wrong_T, "mistake": wrong_mistake, "working": working_T},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the tension in the cable.",
        correct_answer=T, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_T,
        distractors=distractors_T,
        notes=_NOTES,
        scaffold=[] if mode == "constant" else [
            {"prompt": "What is ma (the extra force needed for the acceleration)?", "answer": round(m * a, 2)},
            {"prompt": "What is the tension T?", "answer": T},
        ],
    )

    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    )


def _l3_vertical_inverse(level):
    m = random.randint(5, 40)
    W = _r1(m * G)
    mode = random.choice(["find_a", "find_m"])

    if mode == "find_a":
        a = random.choice([0.3, 0.5, 0.8, 1.0, 1.2, 1.5, 2.0])
        T = _r1(W + m * a)
        question = (
            f"A {_obj()} of mass {m} kg is lifted by a cable with a tension of {T} N. "
            f"Calculate the acceleration of the object."
        )
        working = [
            {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
            {"type": "text",  "content": "Rearrange T = W + ma for acceleration:"},
            {"type": "latex", "content": r"a = \dfrac{T - W}{m}"},
            {"type": "latex", "content": rf"a = \dfrac{{{T} - {W}}}{{{m}}} = {_r1((T - W) / m)}\ \mathrm{{m/s^2}}"},
        ]
        answer = _r1((T - W) / m)
        options_data = [
            {"value": answer, "mistake": None, "working": working},
            {"value": _r1((T + W) / m),
             "mistake": "The weight should be subtracted from the tension, not added. a = (T − W) ÷ m.",
             "working": working},
            {"value": _r1(T / m),
             "mistake": "You forgot to subtract the weight first. a = (T − W) ÷ m.",
             "working": working},
        ]
        scaffold = [
            {"question": "What is the weight W (= mg)?", "answer": W},
            {"question": "What is the acceleration a?", "answer": answer},
        ]
        return make_question(question, answer, options_data, "m/s²",
                             notes=_NOTES, topic="Our Dynamic Universe",
                             question_type="Components of Vectors", level=level, scaffold=scaffold)
    else:
        a = random.choice([0.3, 0.5, 0.8, 1.0, 1.2, 1.5, 2.0])
        mass_true = random.randint(10, 60)
        T = round(mass_true * (G - a), 1)
        answer = _r1(T / (G - a))
        question = (
            f"A winch lowers a box, accelerating downwards at {a} m/s² (less than g, since "
            f"the cable is still under tension). The tension in the cable is {T} N. "
            f"Calculate the mass of the box."
        )
        working = [
            {"type": "latex", "content": r"T = W - ma = mg - ma = m(g - a)"},
            {"type": "latex", "content": rf"m = \dfrac{{T}}{{g - a}} = \dfrac{{{T}}}{{9.8 - {a}}} = {answer}\ \mathrm{{kg}}"},
        ]
        options_data = [
            {"value": answer, "mistake": None, "working": working},
            {"value": _r1(T / (G + a)),
             "mistake": "Since the object accelerates downward (slower than free fall), the denominator is (g − a), not (g + a).",
             "working": working},
            {"value": _r1(T / G),
             "mistake": "You forgot to account for the acceleration — this ignores the fact that the box isn't in free fall or stationary.",
             "working": working},
        ]
        return make_question(question, answer, options_data, "kg",
                             notes=_NOTES, topic="Our Dynamic Universe",
                             question_type="Components of Vectors", level=level)


def _l3_force_from_accel(level="Higher"):
    return random.choice([_l3_horizontal_find_F, _l3_horizontal_find_a,
                           _l3_vertical_given_a, _l3_vertical_inverse])(level)


def gen_rf_l2_balancing_and_accel(level="Higher"):
    """Section 2 — balancing forces, and force from acceleration (horizontal/vertical)."""
    return random.choice([gen_rf_l2_balancing, _l3_force_from_accel])(level)


# ── Level 3 — Weight on a Slope ───────────────────────────────────────────────

def gen_rf_l3_weight_on_slope(level="Higher"):
    m = random.randint(5, 50)
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)

    W = _r1(m * G)
    W_par = _r1(W * math.sin(theta))
    W_perp = _r1(W * math.cos(theta))

    context = f"A {_obj()} of mass {m} kg rests on a ramp inclined at {theta_deg}° to the horizontal."

    working_W = [
        {"type": "latex", "content": r"W = mg"},
        {"type": "latex", "content": rf"W = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the weight of the object.",
        correct_answer=W, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_W,
        distractors=[
            {"value": float(m), "mistake": "Weight is mass × g, not mass on its own.", "working": working_W},
        ],
        notes=_NOTES,
    )

    working_par = [
        {"type": "text",  "content": "The component of weight acting down the slope (parallel to it):"},
        {"type": "latex", "content": r"W_{\parallel} = W\sin\theta"},
        {"type": "latex", "content": rf"W_{{\parallel}} = {W} \times \sin {theta_deg}° = {W_par}\ \mathrm{{N}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the component of the weight acting parallel to (down) the slope.",
        correct_answer=W_par, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_par,
        distractors=[
            {"value": W_perp,
             "mistake": f"The component *parallel* to the slope uses sin θ, not cos θ. W∥ = W sin {theta_deg}° = {W_par} N.",
             "working": working_par},
            {"value": W,
             "mistake": "This is the full weight. It must be resolved using W∥ = W sin θ.",
             "working": working_par},
        ],
        notes=_NOTES,
        scaffold=[
            {"prompt": f"What is sin {theta_deg}°, to 3 decimal places?", "answer": round(math.sin(theta), 3)},
            {"prompt": "What is the component of weight parallel to the slope?", "answer": W_par},
        ],
    )

    return _with_slope_widget(PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    ))


# ── Level 5 — Acceleration on a Slope, With Friction (sliding down) ──────────

def gen_rf_l5_acceleration_with_friction(level="Higher"):
    m = random.randint(5, 40)
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)
    W = _r1(m * G)
    W_par = W * math.sin(theta)
    friction = round(random.uniform(0.2, 0.7) * W_par, 1)
    resultant = _r1(W_par - friction)
    a = _r1(resultant / m)

    obj = _obj()
    question = (
        f"A {obj} of mass {m} kg slides down a slope inclined at {theta_deg}°. Friction "
        f"acts on it with a force of {friction} N, opposing the motion. "
        f"Calculate the acceleration of the {obj}."
    )
    working = [
        {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"W_{{\parallel}} = W\sin\theta = {W} \times \sin {theta_deg}° = {_r1(W_par)}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"\text{{Resultant}} = W_{{\parallel}} - \text{{friction}} = {_r1(W_par)} - {friction} = {resultant}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"a = \dfrac{{\text{{Resultant}}}}{{m}} = \dfrac{{{resultant}}}{{{m}}} = {a}\ \mathrm{{m/s^2}}"},
    ]
    options_data = [
        {"value": a, "mistake": None, "working": working},
        {"value": _r1((W_par + friction) / m),
         "mistake": "Friction opposes the motion down the slope, so it should be subtracted from the parallel weight component, not added.",
         "working": working},
        {"value": _r1(W_par / m),
         "mistake": "You forgot to subtract the friction force before dividing by mass.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is the resultant force along the slope (W∥ − friction)?", "answer": resultant},
        {"question": "What is the acceleration a?", "answer": a},
    ]
    return make_question(question, a, options_data, "m/s²",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Components of Vectors", level=level, scaffold=scaffold)


# ── Level 6 — Finding an Unknown Force (Friction) on a Slope ─────────────────

def gen_rf_l6_unknown_force(level="Higher"):
    m = random.randint(5, 40)
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)
    a = random.choice([0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5])
    W = _r1(m * G)
    W_par = W * math.sin(theta)
    ma = m * a
    friction = _r1(W_par - ma)

    question = (
        f"A {_obj()} of mass {m} kg slides down a slope inclined at {theta_deg}°, "
        f"accelerating at {a} m/s². Calculate the friction force acting on it."
    )
    working = [
        {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"W_{{\parallel}} = W\sin\theta = {W} \times \sin {theta_deg}° = {_r1(W_par)}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"ma = {m} \times {a} = {_r1(ma)}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"\text{{Friction}} = W_{{\parallel}} - ma = {_r1(W_par)} - {_r1(ma)} = {friction}\ \mathrm{{N}}"},
    ]
    options_data = [
        {"value": friction, "mistake": None, "working": working},
        {"value": _r1(W_par + ma),
         "mistake": "Friction opposes the motion, reducing the resultant below the parallel weight component. It should be subtracted, i.e. friction = W∥ − ma.",
         "working": working},
        {"value": _r1(W_par),
         "mistake": "You forgot to subtract ma. friction = W∥ − ma.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is W∥ (= W sinθ)?", "answer": _r1(W_par)},
        {"question": "What is the resultant force along the slope (= ma)?", "answer": _r1(ma)},
        {"question": "What is the friction force?", "answer": friction},
    ]
    return make_question(question, friction, options_data, "N",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Components of Vectors", level=level, scaffold=scaffold)


# ── Level 7 — Finding the Angle of a Slope ────────────────────────────────────

def _l7_direct(level):
    W = random.randint(150, 600)
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)
    W_par = round(W * math.sin(theta), 1)
    sin_theta = round(W_par / W, 3)
    theta_calc = _r1(math.degrees(math.asin(sin_theta)))

    question = (
        f"A crate of weight {W} N rests on a slope. The component of the crate's weight "
        f"acting parallel to the slope is {W_par} N. Calculate the angle of the slope."
    )
    working = [
        {"type": "latex", "content": r"\sin\theta = \dfrac{W_{\parallel}}{W}"},
        {"type": "latex", "content": rf"\sin\theta = \dfrac{{{W_par}}}{{{W}}} = {sin_theta}"},
        {"type": "latex", "content": rf"\theta = \sin^{{-1}}({sin_theta}) = {theta_calc}°"},
    ]
    options_data = [
        {"value": theta_calc, "mistake": None, "working": working},
        {"value": _r1(math.degrees(math.acos(sin_theta))),
         "mistake": "W∥ = W sin θ, so θ must be found using sin⁻¹, not cos⁻¹.",
         "working": working},
        {"value": _r1(W_par / W * 100),
         "mistake": "The angle isn't simply the ratio expressed as a number — you need sin⁻¹ of that ratio.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is sin θ (= W∥ ÷ W)?", "answer": sin_theta},
        {"question": "What is the angle θ?", "answer": theta_calc},
    ]
    return make_question(question, theta_calc, options_data, "°",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Components of Vectors", level=level, scaffold=scaffold)


def _l7_dynamic(level):
    m = random.randint(10, 45)
    friction = random.randint(15, 60)
    constant_speed = random.random() < 0.35
    W = _r1(m * G)

    if constant_speed:
        W_par = float(friction)
        a_text = "the block slides down at a constant speed"
    else:
        a = random.choice([0.5, 0.8, 1.0, 1.2, 1.5, 2.0])
        ma = _r1(m * a)
        W_par = round(ma + friction, 1)
        a_text = f"accelerating at {a} m/s²"

    sin_theta = round(W_par / W, 3)
    if sin_theta >= 1:
        return _l7_dynamic(level)
    theta_calc = _r1(math.degrees(math.asin(sin_theta)))

    obj = _obj()
    question = (
        f"A {obj} of mass {m} kg slides down a slope, {a_text}. The friction force "
        f"acting on the {obj} is {friction} N. Calculate the angle of the slope."
    )
    if constant_speed:
        working = [
            {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
            {"type": "text",  "content": "Constant speed means the forces along the slope are balanced, so W∥ = friction:"},
            {"type": "latex", "content": rf"W_{{\parallel}} = \text{{friction}} = {friction}\ \mathrm{{N}}"},
            {"type": "latex", "content": rf"\sin\theta = \dfrac{{W_{{\parallel}}}}{{W}} = \dfrac{{{W_par}}}{{{W}}} = {sin_theta}"},
            {"type": "latex", "content": rf"\theta = \sin^{{-1}}({sin_theta}) = {theta_calc}°"},
        ]
        scaffold = [
            {"question": "What is W∥, the component of weight parallel to the slope?", "answer": W_par},
            {"question": "What is the angle θ?", "answer": theta_calc},
        ]
    else:
        working = [
            {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
            {"type": "latex", "content": rf"\text{{Resultant}} = ma = {m} \times {a} = {ma}\ \mathrm{{N}}"},
            {"type": "text",  "content": "Rearranging Resultant = W∥ − friction gives the parallel component of weight:"},
            {"type": "latex", "content": rf"W_{{\parallel}} = \text{{Resultant}} + \text{{friction}} = {ma} + {friction} = {W_par}\ \mathrm{{N}}"},
            {"type": "latex", "content": rf"\sin\theta = \dfrac{{W_{{\parallel}}}}{{W}} = \dfrac{{{W_par}}}{{{W}}} = {sin_theta}"},
            {"type": "latex", "content": rf"\theta = \sin^{{-1}}({sin_theta}) = {theta_calc}°"},
        ]
        scaffold = [
            {"question": "What is the resultant (unbalanced) force along the slope (= ma)?", "answer": ma},
            {"question": "What is W∥, the component of weight parallel to the slope?", "answer": W_par},
            {"question": "What is the angle θ?", "answer": theta_calc},
        ]

    options_data = [
        {"value": theta_calc, "mistake": None, "working": working},
        {"value": _r1(math.degrees(math.acos(sin_theta))),
         "mistake": "W∥ = W sin θ, so θ must be found using sin⁻¹, not cos⁻¹.",
         "working": working},
        {"value": _r1(math.degrees(math.asin(min(friction / W, 0.999)))),
         "mistake": "This uses only the friction force. First find W∥, the parallel component of weight, then use sin θ = W∥ ÷ W.",
         "working": working},
    ]
    return make_question(question, theta_calc, options_data, "°",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Components of Vectors", level=level, scaffold=scaffold)


def _l7_find_mass(level):
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)
    friction = random.randint(40, 250)
    W_par = float(friction)
    W = round(W_par / math.sin(theta), 1)
    mass = _r1(W / G)

    question = (
        f"A creel box sits stationary on a slipway inclined at {theta_deg}°, held in place "
        f"by friction alone. The friction force acting up the slope is {friction} N. "
        f"Calculate the component of the box's weight acting parallel to the slope, and "
        f"hence calculate its weight and mass."
    )
    working_par = [
        {"type": "text",  "content": "Held in place by friction alone, so the forces along the slope balance:"},
        {"type": "latex", "content": r"W_{\parallel} = \text{friction}"},
        {"type": "latex", "content": rf"W_{{\parallel}} = {friction}\ \mathrm{{N}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the component of the box's weight acting parallel to the slope.",
        correct_answer=W_par, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_par,
        distractors=[
            {"value": _r1(friction * math.sin(theta)),
             "mistake": f"When stationary and held by friction alone, W∥ equals the friction force exactly — no further resolving is needed: W∥ = {friction} N.",
             "working": working_par},
        ],
        notes=_NOTES,
    )

    working_mass = [
        {"type": "latex", "content": r"W_{\parallel} = W\sin\theta \;\Rightarrow\; W = \dfrac{W_{\parallel}}{\sin\theta}"},
        {"type": "latex", "content": rf"W = \dfrac{{{W_par}}}{{\sin {theta_deg}°}} = {W}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"m = \dfrac{{W}}{{g}} = \dfrac{{{W}}}{{9.8}} = {mass}\ \mathrm{{kg}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Hence calculate the weight and mass of the box.",
        correct_answer=mass, unit="kg",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_mass,
        distractors=[
            {"value": W,
             "mistake": f"That is the weight in newtons, not the mass. Divide by g: m = W ÷ g = {mass} kg.",
             "working": working_mass},
        ],
        notes=_NOTES,
        scaffold=[
            {"prompt": "What is the weight W?", "answer": W},
            {"prompt": "What is the mass m?", "answer": mass},
        ],
    )

    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        is_scenario=True, scenario_context=question, parts=[part_a, part_b],
    )


def _l7_find_angle(level="Higher"):
    return random.choice([_l7_direct, _l7_dynamic, _l7_dynamic, _l7_find_mass])(level)


def gen_rf_l4_slope_dynamics(level="Higher"):
    """Section 4 — acceleration, friction (unknown force), or angle on a slope (sliding down)."""
    q = random.choice([
        gen_rf_l5_acceleration_with_friction,
        gen_rf_l6_unknown_force,
        _l7_find_angle,
    ])(level)
    return _with_slope_widget(q)


# ── Level 5 — Sliding Up a Slope With Friction ────────────────────────────────

def gen_rf_l8_up_slope_deceleration(level="Higher"):
    m = random.randint(10, 45)
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)
    friction = random.randint(10, 60)
    W = _r1(m * G)
    W_par = W * math.sin(theta)
    resultant = _r1(W_par + friction)
    a = _r1(resultant / m)

    obj = _obj()
    context = (
        f"A {obj} of mass {m} kg is given a push and slides up a slope inclined at "
        f"{theta_deg}°. As it slides up, a friction force of {friction} N acts on the "
        f"{obj}, opposing the motion."
    )

    working_res = [
        {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"W_{{\parallel}} = W\sin\theta = {W} \times \sin {theta_deg}° = {_r1(W_par)}\ \mathrm{{N}}"},
        {"type": "text",  "content": "Moving up the slope, both W∥ and friction act down the slope, opposing the motion, so they add together:"},
        {"type": "latex", "content": rf"\text{{Resultant}} = W_{{\parallel}} + \text{{friction}} = {_r1(W_par)} + {friction} = {resultant}\ \mathrm{{N}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the resultant force acting on it along the slope.",
        correct_answer=resultant, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_res,
        distractors=[
            {"value": _r1(W_par - friction),
             "mistake": f"While moving up the slope, friction and W∥ both act down the slope and so must be added, not subtracted. Resultant = W∥ + friction = {resultant} N.",
             "working": working_res},
        ],
        notes=_NOTES,
    )

    working_a = [
        {"type": "latex", "content": r"a = \dfrac{\text{Resultant}}{m}"},
        {"type": "latex", "content": rf"a = \dfrac{{{resultant}}}{{{m}}} = {a}\ \mathrm{{m/s^2}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the deceleration of the object.",
        correct_answer=a, unit="m/s²",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_a,
        distractors=[
            {"value": _r1(W_par / m),
             "mistake": f"This uses W∥ only, ignoring friction. a = Resultant ÷ m = {a} m/s².",
             "working": working_a},
        ],
        notes=_NOTES,
    )

    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    )


def gen_rf_l8_up_slope_find_friction(level="Higher"):
    m = random.randint(10, 45)
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)
    dec = random.choice([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5])
    W = _r1(m * G)
    W_par = W * math.sin(theta)
    ma = m * dec
    friction = _r1(ma - W_par)
    if friction <= 0:
        return gen_rf_l8_up_slope_find_friction(level)

    obj = _obj()
    question = (
        f"A {obj} of mass {m} kg is pushed up a ramp inclined at {theta_deg}° to the "
        f"horizontal. As it slides up, it decelerates at {dec} m/s². Calculate the "
        f"friction force acting on the {obj}."
    )
    working = [
        {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"W_{{\parallel}} = W\sin\theta = {W} \times \sin {theta_deg}° = {_r1(W_par)}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"ma = {m} \times {dec} = {_r1(ma)}\ \mathrm{{N}}"},
        {"type": "text",  "content": "Moving up and decelerating, so both weight component and friction act down the slope:"},
        {"type": "latex", "content": r"ma = W_{\parallel} + \text{friction}"},
        {"type": "latex", "content": rf"\text{{Friction}} = ma - W_{{\parallel}} = {_r1(ma)} - {_r1(W_par)} = {friction}\ \mathrm{{N}}"},
    ]
    options_data = [
        {"value": friction, "mistake": None, "working": working},
        {"value": _r1(ma + W_par),
         "mistake": "Friction and W∥ combine to produce ma while the object moves up the slope, so friction = ma − W∥, not ma + W∥.",
         "working": working},
        {"value": _r1(W_par - ma),
         "mistake": "This gives a negative or mismatched value — while moving up, ma is the larger quantity. friction = ma − W∥.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is W∥ (= W sinθ)?", "answer": _r1(W_par)},
        {"question": "What is the resultant force along the slope (= ma)?", "answer": _r1(ma)},
        {"question": "What is the friction force?", "answer": friction},
    ]
    return make_question(question, friction, options_data, "N",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Components of Vectors", level=level, scaffold=scaffold)


def gen_rf_l8_up_slope_find_angle_or_mass(level="Higher"):
    friction = random.randint(20, 70)
    dec = random.choice([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])

    if random.random() < 0.5:
        m = random.randint(10, 45)
        W = _r1(m * G)
        ma = m * dec
        W_par = round(ma - friction, 1)
        if W_par <= 0 or W_par >= W:
            return gen_rf_l8_up_slope_find_angle_or_mass(level)
        sin_theta = round(W_par / W, 3)
        theta_calc = _r1(math.degrees(math.asin(sin_theta)))

        obj = _obj()
        question = (
            f"A {obj} is pushed up a ramp. A friction force of {friction} N acts on the "
            f"{obj} as it decelerates at {dec} m/s². The {obj} has a mass of {m} kg. "
            f"Calculate the angle of the ramp."
        )
        working = [
            {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
            {"type": "latex", "content": rf"ma = {m} \times {dec} = {_r1(ma)}\ \mathrm{{N}}"},
            {"type": "latex", "content": rf"W_{{\parallel}} = ma - \text{{friction}} = {_r1(ma)} - {friction} = {W_par}\ \mathrm{{N}}"},
            {"type": "latex", "content": rf"\sin\theta = \dfrac{{W_{{\parallel}}}}{{W}} = \dfrac{{{W_par}}}{{{W}}} = {sin_theta}"},
            {"type": "latex", "content": rf"\theta = \sin^{{-1}}({sin_theta}) = {theta_calc}°"},
        ]
        options_data = [
            {"value": theta_calc, "mistake": None, "working": working},
            {"value": _r1(math.degrees(math.acos(sin_theta))),
             "mistake": "W∥ = W sin θ, so θ is found with sin⁻¹, not cos⁻¹.",
             "working": working},
        ]
        scaffold = [
            {"question": "What is the resultant (unbalanced) force along the slope (= ma)?", "answer": _r1(ma)},
            {"question": "What is W∥ (= ma − friction)?", "answer": W_par},
            {"question": "What is the angle θ?", "answer": theta_calc},
        ]
        return make_question(question, theta_calc, options_data, "°",
                             notes=_NOTES, topic="Our Dynamic Universe",
                             question_type="Components of Vectors", level=level, scaffold=scaffold)
    else:
        theta_deg = random.choice(_ANGLES)
        theta = math.radians(theta_deg)
        sin_theta = math.sin(theta)
        denom = dec - G * sin_theta
        if denom <= 0.3:
            return gen_rf_l8_up_slope_find_angle_or_mass(level)
        mass = _r1(friction / denom)
        if not (5 <= mass <= 80):
            return gen_rf_l8_up_slope_find_angle_or_mass(level)

        obj = _obj()
        question = (
            f"A {obj} is pushed up a slipway inclined at {theta_deg}°. A friction force "
            f"of {friction} N acts on the {obj} as it decelerates at {dec} m/s². "
            f"Calculate the mass of the {obj}."
        )
        working = [
            {"type": "latex", "content": r"ma = W_{\parallel} + \text{friction} = mg\sin\theta + \text{friction}"},
            {"type": "latex", "content": r"m(a - g\sin\theta) = \text{friction}"},
            {"type": "latex", "content": rf"m = \dfrac{{\text{{friction}}}}{{a - g\sin\theta}} = \dfrac{{{friction}}}{{{dec} - 9.8\times\sin{theta_deg}°}} = {mass}\ \mathrm{{kg}}"},
        ]
        options_data = [
            {"value": mass, "mistake": None, "working": working},
            {"value": _r1(friction / (dec + G * sin_theta)),
             "mistake": "While moving up the slope, W∥ adds to friction to produce ma, so the denominator is (a − g sin θ), not (a + g sin θ).",
             "working": working},
        ]
        return make_question(question, mass, options_data, "kg",
                             notes=_NOTES, topic="Our Dynamic Universe",
                             question_type="Components of Vectors", level=level)


# ── Level 5b — Constant Applied Force Pushing Up a Slope ─────────────────────
# A continuous applied force F drives the object up the slope, opposed by both
# W∥ and friction (both act down the slope): Resultant = F − W∥ − friction.

def gen_rf_l8_const_force_find_accel(level="Higher"):
    m = random.randint(15, 45)
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)
    W = _r1(m * G)
    W_par = W * math.sin(theta)
    friction = random.randint(15, 60)
    F = round(W_par + friction + random.uniform(20, 120), 0)
    resultant = _r1(F - W_par - friction)
    if resultant <= 0:
        return gen_rf_l8_const_force_find_accel(level)
    a = _r1(resultant / m)

    obj = _obj()
    question = (
        f"A {obj} of mass {m} kg is pulled up a slope inclined at {theta_deg}° by a rope "
        f"providing a constant force of {F:.0f} N up the slope. A friction force of "
        f"{friction} N acts on the {obj} as it slides up. Calculate the acceleration of the {obj}."
    )
    working = [
        {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"W_{{\parallel}} = W\sin\theta = {W} \times \sin {theta_deg}° = {_r1(W_par)}\ \mathrm{{N}}"},
        {"type": "text",  "content": "Both W∥ and friction oppose the applied force F, acting down the slope:"},
        {"type": "latex", "content": r"\text{Resultant} = F - W_{\parallel} - \text{friction}"},
        {"type": "latex", "content": rf"\text{{Resultant}} = {F:.0f} - {_r1(W_par)} - {friction} = {resultant}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"a = \dfrac{{\text{{Resultant}}}}{{m}} = \dfrac{{{resultant}}}{{{m}}} = {a}\ \mathrm{{m/s^2}}"},
    ]
    options_data = [
        {"value": a, "mistake": None, "working": working},
        {"value": _r1((F + W_par + friction) / m),
         "mistake": "W∥ and friction both oppose the applied force here, so they should be subtracted from F, not added.",
         "working": working},
        {"value": _r1(F / m),
         "mistake": "This ignores W∥ and friction, which both act to reduce the resultant force below F.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is W∥ (= W sinθ)?", "answer": _r1(W_par)},
        {"question": "What is the resultant force (= F − W∥ − friction)?", "answer": resultant},
        {"question": "What is the acceleration a?", "answer": a},
    ]
    return make_question(question, a, options_data, "m/s²",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Components of Vectors", level=level, scaffold=scaffold)


def gen_rf_l8_const_force_find_force(level="Higher"):
    m = random.randint(15, 45)
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)
    W = _r1(m * G)
    W_par = W * math.sin(theta)
    friction = random.randint(15, 60)
    constant_speed = random.random() < 0.3

    if constant_speed:
        F = _r1(W_par + friction)
        obj = _obj()
        question = (
            f"A {obj} of mass {m} kg is towed up a slipway at a constant speed, inclined "
            f"at {theta_deg}°. A friction force of {friction} N acts on the {obj}. Calculate "
            f"the size of the constant force required to keep the {obj} moving at a constant "
            f"speed up the slope."
        )
        working = [
            {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
            {"type": "latex", "content": rf"W_{{\parallel}} = W\sin\theta = {W} \times \sin {theta_deg}° = {_r1(W_par)}\ \mathrm{{N}}"},
            {"type": "text",  "content": "Constant speed, so the forces along the slope are balanced:"},
            {"type": "latex", "content": r"F = W_{\parallel} + \text{friction}"},
            {"type": "latex", "content": rf"F = {_r1(W_par)} + {friction} = {F}\ \mathrm{{N}}"},
        ]
        wrong_mistake = f"At constant speed the resultant force is zero, so F must exactly balance W∥ + friction, not just one of them: F = {F} N."
        scaffold = [
            {"question": "What is W∥ (= W sinθ)?", "answer": _r1(W_par)},
            {"question": "What is F (= W∥ + friction)?", "answer": F},
        ]
    else:
        a = random.choice([0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5])
        ma = m * a
        F = _r1(ma + W_par + friction)
        obj = _obj()
        question = (
            f"A {obj} of mass {m} kg is pulled up a slipway inclined at {theta_deg}° by a "
            f"tow rope, accelerating at {a} m/s². A friction force of {friction} N acts on "
            f"the {obj}. Calculate the size of the constant force provided by the rope."
        )
        working = [
            {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
            {"type": "latex", "content": rf"W_{{\parallel}} = W\sin\theta = {W} \times \sin {theta_deg}° = {_r1(W_par)}\ \mathrm{{N}}"},
            {"type": "latex", "content": rf"\text{{Resultant}} = ma = {m} \times {a} = {_r1(ma)}\ \mathrm{{N}}"},
            {"type": "latex", "content": r"F = \text{Resultant} + W_{\parallel} + \text{friction}"},
            {"type": "latex", "content": rf"F = {_r1(ma)} + {_r1(W_par)} + {friction} = {F}\ \mathrm{{N}}"},
        ]
        wrong_mistake = f"F must overcome W∥ and friction *and* provide the resultant force for the acceleration — all three add together: F = {F} N."
        scaffold = [
            {"question": "What is the resultant (unbalanced) force needed for this acceleration (= ma)?", "answer": _r1(ma)},
            {"question": "What is W∥ (= W sinθ)?", "answer": _r1(W_par)},
            {"question": "What is F (= Resultant + W∥ + friction)?", "answer": F},
        ]

    options_data = [
        {"value": F, "mistake": None, "working": working},
        {"value": _r1(W_par + friction) if constant_speed else _r1(ma + W_par),
         "mistake": wrong_mistake,
         "working": working},
    ]
    return make_question(question, F, options_data, "N",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Components of Vectors", level=level, scaffold=scaffold)


def gen_rf_l8_const_force_find_friction(level="Higher"):
    m = random.randint(15, 45)
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)
    W = _r1(m * G)
    W_par = W * math.sin(theta)
    a = random.choice([0.5, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0])
    ma = m * a
    F = round(W_par + ma + random.uniform(20, 100), 0)
    friction = _r1(F - W_par - ma)
    if friction <= 0:
        return gen_rf_l8_const_force_find_friction(level)

    obj = _obj()
    question = (
        f"A {obj} of mass {m} kg is pushed up a ramp inclined at {theta_deg}° by a constant "
        f"force of {F:.0f} N, accelerating at {a} m/s². Calculate the friction force acting "
        f"on the {obj}."
    )
    working = [
        {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"W_{{\parallel}} = W\sin\theta = {W} \times \sin {theta_deg}° = {_r1(W_par)}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"\text{{Resultant}} = ma = {m} \times {a} = {_r1(ma)}\ \mathrm{{N}}"},
        {"type": "text",  "content": "F drives the object up the slope, opposed by both W∥ and friction:"},
        {"type": "latex", "content": r"F = \text{Resultant} + W_{\parallel} + \text{friction}"},
        {"type": "latex", "content": rf"\text{{Friction}} = F - \text{{Resultant}} - W_{{\parallel}} = {F:.0f} - {_r1(ma)} - {_r1(W_par)} = {friction}\ \mathrm{{N}}"},
    ]
    options_data = [
        {"value": friction, "mistake": None, "working": working},
        {"value": _r1(F - W_par + ma),
         "mistake": "The resultant force (ma) is what's left of F after overcoming W∥ and friction — it should be subtracted along with W∥, not added.",
         "working": working},
        {"value": _r1(F - ma),
         "mistake": "You forgot to subtract W∥ as well. Friction = F − Resultant − W∥.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is W∥ (= W sinθ)?", "answer": _r1(W_par)},
        {"question": "What is the resultant force (= ma)?", "answer": _r1(ma)},
        {"question": "What is the friction force?", "answer": friction},
    ]
    return make_question(question, friction, options_data, "N",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Components of Vectors", level=level, scaffold=scaffold)


def gen_rf_l8_const_force_find_angle(level="Higher"):
    m = random.randint(15, 45)
    F = random.randint(150, 320)
    a = random.choice([0.5, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0, 2.5])
    friction = random.randint(15, 60)
    W = _r1(m * G)
    ma = m * a
    W_par = round(F - ma - friction, 1)
    if W_par <= 0 or W_par >= W:
        return gen_rf_l8_const_force_find_angle(level)
    sin_theta = round(W_par / W, 3)
    theta_calc = _r1(math.degrees(math.asin(sin_theta)))

    obj = _obj()
    question = (
        f"A {obj} of mass {m} kg is winched up a slipway by a constant force of {F} N, "
        f"accelerating at {a} m/s². A friction force of {friction} N acts on the {obj}. "
        f"Calculate the angle of the slipway."
    )
    working = [
        {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"\text{{Resultant}} = ma = {m} \times {a} = {_r1(ma)}\ \mathrm{{N}}"},
        {"type": "latex", "content": r"F = \text{Resultant} + W_{\parallel} + \text{friction} \;\Rightarrow\; W_{\parallel} = F - \text{Resultant} - \text{friction}"},
        {"type": "latex", "content": rf"W_{{\parallel}} = {F} - {_r1(ma)} - {friction} = {W_par}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"\sin\theta = \dfrac{{W_{{\parallel}}}}{{W}} = \dfrac{{{W_par}}}{{{W}}} = {sin_theta}"},
        {"type": "latex", "content": rf"\theta = \sin^{{-1}}({sin_theta}) = {theta_calc}°"},
    ]
    options_data = [
        {"value": theta_calc, "mistake": None, "working": working},
        {"value": _r1(math.degrees(math.acos(sin_theta))),
         "mistake": "W∥ = W sin θ, so θ is found with sin⁻¹, not cos⁻¹.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is the resultant force (= ma)?", "answer": _r1(ma)},
        {"question": "What is W∥ (= F − Resultant − friction)?", "answer": W_par},
        {"question": "What is the angle θ?", "answer": theta_calc},
    ]
    return make_question(question, theta_calc, options_data, "°",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Components of Vectors", level=level, scaffold=scaffold)


def gen_rf_l5_up_slope(level="Higher"):
    """Section 5 — object sliding up a slope with friction: pushed-once (decelerating)
    or driven by a constant applied force (deceleration/friction/angle/mass either way)."""
    q = random.choice([
        gen_rf_l8_up_slope_deceleration,
        gen_rf_l8_up_slope_find_friction,
        gen_rf_l8_up_slope_find_angle_or_mass,
        gen_rf_l8_const_force_find_accel,
        gen_rf_l8_const_force_find_force,
        gen_rf_l8_const_force_find_friction,
        gen_rf_l8_const_force_find_angle,
    ])(level)
    return _with_slope_widget(q)


# ── Level 6 — Explain: Effect of Angle ────────────────────────────────────────

def _explain_tension(level):
    obj = _obj()
    context = (
        f"A {obj} is held stationary on a smooth (frictionless) slope by a rope running "
        f"parallel to the slope. The angle of the slope is then increased, while the mass "
        f"of the {obj} stays the same."
    )
    question_text = "What happens to the tension in the rope, and why?"
    correct = (
        "The tension increases, because the rope must balance the component of weight "
        "acting down the slope, W sin θ, and sin θ increases as the angle increases."
    )
    working = [
        {"type": "text", "content": (
            f"With no friction, the rope's tension must exactly balance the parallel "
            f"component of the {obj}'s weight: T = W sin θ. As θ increases (up to 90°), "
            "sin θ increases, so T must increase too."
        )},
    ]
    distractors = [
        {"value": "The tension decreases, because less of the weight acts along the slope as the angle increases.",
         "mistake": "It's the opposite — as the slope gets steeper, *more* of the weight acts down the slope (W sin θ increases with θ), so the tension needed increases.",
         "working": working},
        {"value": "The tension stays the same, because the weight of the object doesn't change.",
         "mistake": "The weight itself doesn't change, but the *component* of that weight acting down the slope does — W sin θ depends on the angle, not just on W.",
         "working": working},
        {"value": "The tension increases, because the normal force from the slope increases as the angle increases.",
         "mistake": "The normal force (perpendicular component, W cos θ) actually decreases as the angle increases — it isn't what determines the tension here.",
         "working": working},
    ]
    return context, question_text, correct, distractors


def _explain_mass_parallel(level):
    obj = _obj()
    context = (
        f"Two identical {obj}s are placed on the same slope, at the same angle. One {obj} "
        f"has twice the mass of the other."
    )
    question_text = "How does the component of weight acting parallel to the slope compare for the two objects, and why?"
    correct = (
        "It is twice as large for the heavier object, because W∥ = W sin θ = mg sin θ, and "
        "for a fixed angle this component is directly proportional to mass."
    )
    working = [
        {"type": "text", "content": (
            "The parallel component of weight is W∥ = mg sin θ. For the same angle θ, W∥ "
            "is directly proportional to mass m, so doubling the mass doubles W∥."
        )},
    ]
    distractors = [
        {"value": "It is the same for both objects, because the angle of the slope hasn't changed.",
         "mistake": "The angle being the same doesn't mean W∥ is the same — W∥ = mg sin θ also depends on mass, which has doubled.",
         "working": working},
        {"value": "It is four times as large for the heavier object, since weight depends on mass squared.",
         "mistake": "Weight is W = mg — mass appears only to the first power, not squared. Doubling m doubles W, and so doubles W∥ = W sin θ too.",
         "working": working},
        {"value": "It cannot be compared without knowing the coefficient of friction.",
         "mistake": "Friction doesn't affect the weight component itself — W∥ = mg sin θ depends only on mass and angle.",
         "working": working},
    ]
    return context, question_text, correct, distractors


def _explain_wpar_increases(level):
    obj = _obj()
    context = (
        f"A {obj} rests on a ramp used to load a ferry. The angle of the ramp is then "
        f"increased, while the mass of the {obj} stays the same."
    )
    question_text = "What happens to the component of the crate's weight acting parallel to the ramp, and why?"
    correct = (
        "It increases, because W∥ = W sin θ, and sin θ increases as the angle increases "
        "(up to 90°)."
    )
    working = [
        {"type": "text", "content": (
            "W∥ = W sin θ. The weight W itself doesn't change, but as θ increases, sin θ "
            "increases, so the component of weight acting down the slope increases."
        )},
    ]
    distractors = [
        {"value": "It decreases, because less of the weight acts along a steeper ramp.",
         "mistake": "It's the opposite — a steeper ramp means *more* of the weight acts along it. sin θ increases as θ increases, so W∥ increases.",
         "working": working},
        {"value": "It stays the same, because the weight of the crate doesn't change.",
         "mistake": "The weight itself doesn't change, but its *component* along the ramp does — W∥ = W sin θ depends on angle as well as weight.",
         "working": working},
        {"value": "It increases initially, then decreases once the ramp is steep enough.",
         "mistake": "sin θ increases continuously as θ increases from 0° to 90°, so W∥ keeps increasing throughout this range.",
         "working": working},
    ]
    return context, question_text, correct, distractors


def _explain_vertical_tension(level):
    context = (
        "A tractor tows a sledge using a rope of constant tension. The angle the rope "
        "makes with the ground is then increased."
    )
    question_text = "What happens to the vertical component of the tension, and why?"
    correct = (
        "It increases, because Fy = T sin θ, and sin θ increases as the angle increases, "
        "even though the tension T itself is unchanged."
    )
    working = [
        {"type": "text", "content": (
            "Fy = T sin θ. Since T is constant, Fy depends only on sin θ. As θ increases "
            "(up to 90°), sin θ increases, so the vertical component increases."
        )},
    ]
    distractors = [
        {"value": "It decreases, because the horizontal component takes up more of the tension at a steeper angle.",
         "mistake": "The horizontal component (T cos θ) does decrease, but the vertical component (T sin θ) increases — they don't trade off in the way suggested.",
         "working": working},
        {"value": "It stays the same, because the tension in the rope hasn't changed.",
         "mistake": "The tension T is unchanged, but its *vertical component* Fy = T sin θ still depends on the angle, which has increased.",
         "working": working},
        {"value": "It cannot be determined without knowing the mass of the sledge.",
         "mistake": "The vertical component of a given tension depends only on the tension and the angle — Fy = T sin θ — not on the sledge's mass.",
         "working": working},
    ]
    return context, question_text, correct, distractors


def _explain_accel_decreases(level):
    obj = _obj()
    context = (
        f"A {obj} slides down a slope with a constant friction force acting on it. The "
        f"angle of the slope is then decreased."
    )
    question_text = "What happens to the acceleration of the block, and why?"
    correct = (
        "It decreases, because the resultant force along the slope is W∥ − friction = "
        "mg sin θ − friction, and as θ decreases, sin θ decreases so W∥ decreases while "
        "friction stays the same, reducing the resultant force and hence the acceleration."
    )
    working = [
        {"type": "text", "content": (
            "a = (mg sin θ − friction) ÷ m. As θ decreases, sin θ decreases, so W∥ = mg sin θ "
            "decreases. Since friction is unchanged, the resultant force W∥ − friction gets "
            "smaller, so the acceleration decreases."
        )},
    ]
    distractors = [
        {"value": "It increases, because the friction force has more effect on a gentler slope.",
         "mistake": "Friction stays the same regardless of angle here — it's W∥ that shrinks as the slope becomes gentler, reducing the resultant force and the acceleration.",
         "working": working},
        {"value": "It stays the same, because friction is constant.",
         "mistake": "Friction being constant doesn't mean the resultant force is constant — W∥ = mg sin θ still changes with angle, and it's the resultant of W∥ and friction that sets the acceleration.",
         "working": working},
        {"value": "It decreases to zero immediately, since a smaller angle means no motion is possible.",
         "mistake": "A smaller angle reduces the acceleration, but doesn't necessarily make it zero — that only happens if W∥ becomes exactly equal to (or less than) the friction force.",
         "working": working},
    ]
    return context, question_text, correct, distractors


def _explain_weight_constant(level):
    obj = _obj()
    context = f"A {obj} of fixed mass is placed on ramps of different angles, one after another."
    question_text = "What happens to the crate's weight as the ramp angle changes, and why?"
    correct = (
        "It stays the same, because weight is W = mg, which depends only on mass and g — "
        "not on the angle of the ramp."
    )
    working = [
        {"type": "text", "content": (
            "Weight W = mg depends only on mass and the gravitational field strength g, "
            "neither of which changes when the ramp's angle changes. Changing the angle "
            "changes how the weight is *resolved* into components, but not the weight itself."
        )},
    ]
    distractors = [
        {"value": "It increases as the ramp angle increases, since more of the crate's weight is needed to hold it in place.",
         "mistake": "This confuses weight with the parallel component of weight (W∥ = W sin θ), which does change with angle — the weight itself, W = mg, does not.",
         "working": working},
        {"value": "It decreases as the ramp angle increases, because the normal force supports more of it.",
         "mistake": "The normal force (W cos θ) does decrease with angle, but that doesn't change the crate's actual weight — W = mg is fixed.",
         "working": working},
        {"value": "It depends on the angle, because weight is a component of the resolved force system.",
         "mistake": "Weight is the original force being resolved, not one of its components — W = mg is independent of how it's later split into W∥ and W⊥.",
         "working": working},
    ]
    return context, question_text, correct, distractors


def gen_rf_l6_explain_angle(level="Higher"):
    builder = random.choice([
        _explain_tension, _explain_mass_parallel, _explain_wpar_increases,
        _explain_vertical_tension, _explain_accel_decreases, _explain_weight_constant,
    ])
    context, question_text, correct, distractors = builder(level)

    options = [correct] + [d["value"] for d in distractors]
    random.shuffle(options)

    part = PhysicsQuestion(
        question_text=question_text,
        correct_answer=correct,
        unit="",
        topic="Our Dynamic Universe",
        question_type="Components of Vectors",
        level=level,
        distractors=distractors,
        working=distractors[0]["working"],
        notes=_NOTES,
        metadata={"type": "classification", "options": options},
    )

    return _with_slope_widget(PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        is_scenario=True, scenario_context=context, parts=[part],
    ))
