from decimal import Decimal
from hummingbot.strategy.market_trading_pair_tuple import MarketTradingPairTuple
from hummingbot.strategy.amm_arb.amm_arb import AmmArbStrategy
from hummingbot.strategy.amm_arb.amm_arb_config_map import amm_arb_config_map


def start(self):
    market_tuples = amm_arb_config_map.get("market_list").value
    order_amount = amm_arb_config_map.get("order_amount").value
    min_profitability = amm_arb_config_map.get("min_profitability").value / Decimal("100")
    market_1_slippage_buffer = amm_arb_config_map.get("market_1_slippage_buffer").value / Decimal("100")
    market_2_slippage_buffer = amm_arb_config_map.get("market_2_slippage_buffer").value / Decimal("100")
    market_3_slippage_buffer = amm_arb_config_map.get("market_3_slippage_buffer").value / Decimal("100")
    concurrent_orders_submission = amm_arb_config_map.get("concurrent_orders_submission").value

    self._initialize_markets([(connector.lower(), [market]) for (connector, market) in market_tuples])
    bases = [market.split("-")[0] for (_, market) in market_tuples]
    quotes = [market.split("-")[1] for (_, market) in market_tuples]
    self.assets = set(bases + quotes)

    markets_info = [MarketTradingPairTuple(self.markets[connector.lower()], market, base, quote) for ((connector, market), base, quote) in zip(market_tuples, bases, quotes)]

    self.market_trading_pair_tuples = markets_info
    self.strategy = AmmArbStrategy(markets_info, min_profitability, order_amount,
                                   [market_1_slippage_buffer, market_2_slippage_buffer, market_3_slippage_buffer],
                                   concurrent_orders_submission)
