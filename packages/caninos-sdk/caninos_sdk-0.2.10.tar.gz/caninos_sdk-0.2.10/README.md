# Caninos SDK

Estamos criando uma SDK para fazer com que o uso da Labrador fique **muito acessível**.
O objetivo é permitir códigos assim:

```python
# as 4 linhas abaixo já funcionam:
import caninos_sdk as k9
labrador = k9.Labrador()
labrador.pin15.enable_gpio(k9.Pin.Direction.OUTPUT, alias="led_status")
labrador.pin19.enable_gpio(k9.Pin.Direction.INPUT, alias="button1")
labrador.camera.enable()

# as próximas 5 ainda não (precisa ser desenvolvido)
labrador.pin.enable_gpio(k9.cpu_pin(0x33), k9.INPUT, alias="button1")
labrador.pin.enable_gpio(7, k9.I2C, address=0x4, alias="temp_sensor1")
labrador.pin.enable_gpio(9, k9.SPI, address=0x4, alias="temp_sensor2")
labrador.wifi.enable("CITI", "1cbe991a14")

print(labrador.enabled_features())

# uso
labrador.led_status.high() # já funciona
res = labrador.button1.read() # já funciona
value = labrador.temp_sensor1.read() # ainda não

ip = labrador.wifi.get_ip() # ainda não
ok, frame = labrador.camera.read() # já funciona
```

Caso queira ajudar com a implementação, dê uma olhadinha nos [issues](https://github.com/caninos-loucos/caninos-sdk/issues).

# Começando

**⚠️ Atenção**: para usar as GPIOs sem `sudo`, é necessário fazer a configuração abaixo uma única vez (será mantido quando reiniciar a placa):

```bash
sudo chmod +x ./gpio-config.sh
sudo ./gpio-config.sh
```

## Piscando um LED - o Hello World do hardware

```python
# importa a SDK e dá a ela um apelido bonitinho
import caninos_sdk as k9

# instancia o objeto labrador
labrador = k9.Labrador()

# habilita o pino 15 como saída, e dá a ele o apelido "led_status"
labrador.pin15.enable_gpio(k9.Pin.Direction.OUTPUT, alias="led_status")

# liga o "led_status"
labrador.led_status.high()
# desliga o "led_status"
labrador.led_status.low()
# liga o mesmo led de novo, porém agora se referindo a ele pelo número do pino
labrador.pin15.high()
```

## Outros exemplos

Confira a pasta [examples](https://github.com/caninos-loucos/caninos-sdk/tree/main/examples) do repositório no GitHub.

**⚠️ Atenção**: para usar a câmera, é necessário instalar o [OpenCV](https://linuxize.com/post/how-to-install-opencv-on-debian-10/). Instale-o com o comando abaixo:
- `sudo apt install python3-opencv`

# Contributing

First, see the [issues](https://github.com/caninos-loucos/caninos-sdk/issues) page.

Then, install some dependencies:

```bash
sudo apt install python3-dev python3-pip python3-setuptools libffi-dev libssl-dev curl
pip3 install --upgrade pip
```

Finally, install the package locally in _editable_ form:
```bash
pip3 install -e .
```


## Publish a new version
Install build deps: `pip3 install build twine`.

Update the version number at `__init__.py`.

```bash
# build the new version
python3 -m build

# deploy
VERSION=$(grep -r "__version__" caninos_sdk/__init__.py | sed -E 's/.* = "(.*)"/\1/g')
twine upload dist/caninos_sdk-$VERSION-py3-none-any.whl  --config-file ${HOME}/.pypirc
```


## TO-DO:
- [x] initial sketch to prove the concept
- [x] make the gpios actually work (read/write)
~~- [ ] create default constructors/subclasses for specific boards~~
~~- [ ] create a "VirtualLabrador" class, for tests and remote labs~~
- [x] refactor to a proper python package using modern python conventions
- [-] write unit tests -> works with `pytest -s`
- [x] gpio read/write work across Labradors 32/64
- [x] support pwm
- [ ] support i2c
- [ ] support spi
- [ ] support wifi
- [x] support camera

Other notes:
- should this library support other SBCs?
- should the docs be in English or Portuguese?
- need to get funding or community help
