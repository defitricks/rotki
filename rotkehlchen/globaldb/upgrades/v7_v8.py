from typing import TYPE_CHECKING, Final

from rotkehlchen.logging import enter_exit_debug_log
from rotkehlchen.utils.misc import ts_now

if TYPE_CHECKING:
    from rotkehlchen.db.drivers.gevent import DBConnection, DBCursor


ASSETS_TO_WHITELIST: Final = (
    'eip155:1/erc20:0x2ecB13A8c458c379c4d9a7259e202De03c8F3D19',  # Block-Chain.com(BC)
    'eip155:1/erc20:0xA0b73E1Ff0B80914AB6fe0444E65848C4C34450b',  # Crypto.com Chain(CRO)
    'eip155:1/erc20:0xB70835D7822eBB9426B56543E391846C107bd32C',  # Game.com(GTC)
    'eip155:1/erc20:0x9C78EE466D6Cb57A4d01Fd887D2b5dFb2D46288f',  # MUST (Cometh)(MUST)
    'eip155:1/erc20:0xB63B606Ac810a52cCa15e44bB630fd42D8d1d83d',  # Crypto.com(MCO)
    'eip155:1/erc20:0x905E337c6c8645263D3521205Aa37bf4d034e745',  # doc.com Token(MTC)
    'eip155:1/erc20:0x6863bE0e7CF7ce860A574760e9020D519a8bDC47',  # On.Live(ONL)
    'eip155:1/erc20:0x9B02dD390a603Add5c07f9fd9175b7DABE8D63B7',  # Shopping.io(SPI)
    'eip155:1/erc20:0xD6Ea40597Be05c201845c0bFd2e96A60bACde267',  # Curve Compound Pool yVault(yvCurve-Compound)  # noqa: E501
    'eip155:1/erc20:0xf2db9a7c0ACd427A680D640F02d90f6186E71725',  # Curve LINK Pool yVault(yvCurve-LINK)  # noqa: E501
    'eip155:1/erc20:0x50f09629d0afDF40398a3F317cc676cA9132055c',  # EVAI.IO(EVAI)
    'eip155:1/erc20:0xd3E4Ba569045546D09CF021ECC5dFe42b1d7f6E4',  # Morpheus.Network(MNW)
    'eip155:137/erc20:0xd7c8469c7eC40f853dA5f651DE81b45aeD47e5aB',  # PotCoin.com POT(POT)
    'eip155:43114/erc20:0xbd3936eC8D83A5D4e73ecA625eCFa006da8C8F52',  # UREEQA Token [via ChainPort.io](URQA)  # noqa: E501
    'eip155:56/erc20:0xCB6409696c58aA777317dbdfaa8bab4AC8e39Eea',  # PeerEx_Network(PERX)
    'eip155:56/erc20:0x78A18Db278F9c7c9657F61dA519e6Ef43794DD5D',  # Shopping.io on BSC(SPI)
    'eip155:56/erc20:0x39d4549908e7Adcee9b439429294eEb4c65c2C9e',  # Chainport.io-Peg HORD Token(HORD)  # noqa: E501
    'eip155:56/erc20:0x431e0cD023a32532BF3969CddFc002c00E98429d',  # Chainport.io-Peg XCAD Token(XCAD)  # noqa: E501
    'eip155:56/erc20:0x959229D94c9060552daea25AC17193bcA65D7884',  # IOI Token via ChainPort.io(IOI)  # noqa: E501
    'eip155:56/erc20:0x686318000d982bc8dCC1cdCF8fFd22322F0960Ed',  # OpulousToken [via ChainPort.io](OPUL)  # noqa: E501
    'eip155:56/erc20:0x9CD9C5a44CB8fab39b2Ee3556F5c439e65E4fDdD',  # MARS4 [via ChainPort.io](MARS4)  # noqa: E501
    'eip155:56/erc20:0xeCEB87cF00DCBf2D4E2880223743Ff087a995aD9',  # NUM Token [via ChainPort.io](NUM)  # noqa: E501
    'eip155:56/erc20:0x368ce786Ea190f32439074e8d22e12ecb718B44c',  # Epik Prime [via ChainPort.io](EPIK)  # noqa: E501
    'eip155:56/erc20:0x0F5d8CD195a4539bcf2eC6118C6dA50287c6d5f5',  # Gold Fever Native Gold [via ChainPort.io](NGL)  # noqa: E501
    'eip155:56/erc20:0x52fe7b439753092f584917e3EFEa86A1cFD210f9',  # Trazable [via ChainPort.io](TRZ)  # noqa: E501
    'eip155:56/erc20:0x3a06212763CAF64bf101DaA4b0cEbb0cD393fA1a',  # Chainport.io-Peg delta.theta(DLTA)  # noqa: E501
    'eip155:56/erc20:0x6a6Ccf15B38DA4b5B0eF4C8fe9FefCB472A893F9',  # MoonStarter.net(MNST)
    'eip155:56/erc20:0xBd2949F67DcdC549c6Ebe98696449Fa79D988A9F',  # Wrapped MTRG on BSC by Meter.io(MTRG)  # noqa: E501
    'eip155:56/erc20:0x2235e79086dd23135119366da45851c741874e5B',  # CREDI [via ChainPort.io](CREDI)  # noqa: E501
    'eip155:1/erc20:0x4185cf99745B2a20727B37EE798193DD4a56cDfa',  # DEUS Synthetic Coinbase IOU(wCOINBASE-IOU)  # noqa: E501
    'eip155:1/erc20:0x1c899dED01954d0959E034b62a728e7fEbE593b0',  # Curve.fi Factory Plain Pool: stLINK/LINK(stLINK-f)  # noqa: E501
    'eip155:1/erc20:0xc56c2b7e71B54d38Aab6d52E94a04Cbfa8F604fA',  # Z.com USD(ZUSD)
    'eip155:1/erc20:0x96Ea6AF74Af09522fCB4c28C269C26F59a31ced6',  # curve.fi/link(yvlinkCRV)
    'eip155:1/erc20:0x4f018C06810Ea979F0E8a5D73CB8aa977Ba17aBA',  # Curve.fi Factory Crypto Pool: EtherTulip.com(PETAL-f)  # noqa: E501
    'eip155:1/erc20:0xc29259ea3f13778B8985014fB4b1b8e7DC5d5C94',  # Curve.fi Factory Crypto Pool: EtherTulip.com(PETALrai-f)  # noqa: E501
    'eip155:1/erc20:0x1974e843Fcf3627f8999544F3842bF58BB921ca2',  # Curve.fi Factory Crypto Pool: liq_ETH_LINK(ETH LINK-f)  # noqa: E501
    'eip155:1/erc20:0x5b1FDc01f028C2347ab5fddB4D1effBf82a411d3',  # Curve.fi Factory Crypto Pool: liq_CRV_LINK(CRV LINK-f)  # noqa: E501
    'eip155:1/erc20:0x6BC08509B36A98E829dFfAD49Fde5e412645d0a3',  # WoofWork.io(WOOF)
    'eip155:1/erc20:0xA49d7499271aE71cd8aB9Ac515e6694C755d400c',  # Mute.io(MUTE)
    'eip155:10/erc20:0xb396b31599333739A97951b74652c117BE86eE1D',  # Davos.xyz USD(DUSD)
    'eip155:1/erc20:0xaA247c0D81B83812e1ABf8bAB078E4540D87e3fB',  # meson.network(MSN)
)


@enter_exit_debug_log()
def fix_detected_spam_tokens(write_cursor: 'DBCursor') -> None:
    """Remove assets marked as spam by error and whitelist them"""
    write_cursor.executemany(
        'UPDATE evm_tokens SET protocol=NULL WHERE identifier=?',
        [(asset_id,) for asset_id in ASSETS_TO_WHITELIST],
    )
    current_ts = ts_now()
    write_cursor.executemany(
        'INSERT OR IGNORE INTO general_cache(key, value, last_queried_ts) VALUES (?, ?, ?)',
        [('SPAM_ASSET_FALSE_POSITIVE', asset_id, current_ts) for asset_id in ASSETS_TO_WHITELIST],
    )


@enter_exit_debug_log(name='globaldb v7->v8 upgrade')
def migrate_to_v8(connection: 'DBConnection') -> None:
    """This globalDB upgrade does the following:
    - Fix autodetected spam assets by mistake

    This upgrade takes place in v1.34.0"""
    with connection.write_ctx() as write_cursor:
        fix_detected_spam_tokens(write_cursor)
