"""
"""

import re
import json

from rio_tiler import main
from rio_tiler.utils import array_to_img, linear_rescale
import numpy as np
from lambda_proxy.proxy import API
from distutils import util

APP = API(app_name="lambda-tiler")


@APP.route('/bounds', methods=['GET'], cors=True)
def bounds():
    """
    Handle bounds requests
    """

    query_args = APP.current_request.query_params
    query_args = query_args if isinstance(query_args, dict) else {}

    address = query_args['url']
    info = main.bounds(address)
    return ('OK', 'application/json', json.dumps(info))


@APP.route('/tiles/<int:z>/<int:x>/<int:y>.<ext>', methods=['GET'], cors=True)
def tile(tile_z, tile_x, tile_y, tileformat):
    """
    Handle tile requests
    """
    query_args = APP.current_request.query_params
    query_args = query_args if isinstance(query_args, dict) else {}

    address = query_args['url']

    bands = query_args.get('rgb')
    if bands:
        bands = tuple(int(s) for s in re.findall(r'\d+', bands))

    tilesize = query_args.get('tile', 512)
    tilesize = int(tilesize) if isinstance(tilesize, str) else tilesize

    nodata = query_args.get('nodata')
    if nodata is not None:
        nodata = int(nodata)

    alpha = query_args.get('alpha')
    if alpha is not None:
        alpha = int(alpha)

    # detect linear scale request
    linearStretch = query_args.get('linearStretch')


    tile, mask = main.tile(address, tile_x, tile_y, tile_z, bands, tilesize=tilesize, nodata=nodata, alpha=alpha)

    if linearStretch is not None:
        if util.strtobool(linearStretch):
            tile = linear_rescale(tile,
                           in_range=(np.min(tile), np.max(tile))
                           )

    tile = array_to_img(tile, tileformat, mask=mask)


    if tileformat == 'jpg':
        tileformat = 'jpeg'

    return ('OK', f'image/{tileformat}', tile)


@APP.route('/NDtiles/<int:z>/<int:x>/<int:y>.<ext>', methods=['GET'], cors=True)
def NDtile(tile_z, tile_x, tile_y, tileformat):
    """
    Handle tile requests
    """
    query_args = APP.current_request.query_params
    query_args = query_args if isinstance(query_args, dict) else {}

    address = query_args['url']

    # get Band indexes
    band1 = query_args.get('band1')
    band2 = query_args.get('band2')
    if band1 & band2:
        bands = (band1, band2)
    else:
        raise ("Error No Bnads specified")

    tilesize = query_args.get('tile', 512)
    tilesize = int(tilesize) if isinstance(tilesize, str) else tilesize

    nodata = query_args.get('nodata')
    if nodata is not None:
        nodata = int(nodata)

    alpha = query_args.get('alpha')
    if alpha is not None:
        alpha = int(alpha)


    tile, mask = main.tile(address, tile_x, tile_y, tile_z, bands, tilesize=tilesize, nodata=nodata, alpha=alpha)

    bandTile1 = tile[:,:,0]
    bandTile2 = tile[:, :, 1]

    np.seterr(divide='ignore', invalid='ignore')
    tile = (band2.astype(float) - band1.astype(float)) / (band2.astype(float) + band1.astype(float))

    # detect linear scale request
    linearStretch = query_args.get('linearStretch')
    if linearStretch:
        if util.strtobool(linearStretch):
            tile = linear_rescale(tile,
                                   in_range=(-1, 1)
                                   )

    tile = array_to_img(tile, tileformat, mask=mask)


    if tileformat == 'jpg':
        tileformat = 'jpeg'

    return ('OK', f'image/{tileformat}', tile)




@APP.route('/favicon.ico', methods=['GET'], cors=True)
def favicon():
    """
    favicon
    """
    return('NOK', 'text/plain', '')
