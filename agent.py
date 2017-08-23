#!/usr/bin/env python3

import typing
from finance import *

class Individual:
    '''The most base-level human
    resources available  >>> MAXIMIZE (success condition)

    DATA
        have a need (sustenance)  >>> FAILURE if supply falls below threshold.  
        have a rate of consumption (eventually maybe control that to a point)
    '''

    def __init__(self, name: str, resources: int, need: int, roc: int) -> None:
        self.name = name
        self.need = need
        self.resources = resources
        self.roc = roc

        if not self.roc:
            self.roc = 1  # TODO(willie): randomize

    def fail(self) -> bool:
        if self.need <= 0:
            return True
        return False

    def consume(self) -> bool:
        self.need -= self.roc
        return not self.fail()


class Consumer(Individual):
    '''The base class for all consumers

    DATA
        eventually have wants?

    ACTIONS
        ability to buy
             determine product and amount of that product to buy
             find an agent that can fulfill its need
                  ask the Market for a list of sellers?
             negotiate a deal with that agent
             finalize the transaction
    '''
    
    def __init__(self, name, resources, need, roc=None) -> None:
        super().__init__(name, resources, need, roc)

    def buy(self, market, product, amount):  # TODO(willie): flesh this out
        # this product and amount make the Consumer's ideal purchase.  We now try to get close to that
        offers = market.get_advertisements(product)
        offers = [o for o in offer if o.stock >= amount]
        possible_deals = [self.best_deal(offer) for offer in offers]
        deal = self.choose_deal(possible_deals)
        if self.make_deal(deal, market):
            return deal
        else: return None

    def best_deal(self, offer: Offer) -> Offer:
        #negotiate with seller
        pass

    def choose_deal(self, possible_deals: List[Offer]) -> Offer:
        #best price for amount that is close to what we want
        pass

    def make_deal(self, deal: Offer, market: MarketClient) -> bool:
        if not deal:
            return False
        pass
        #make the deal using the market as a proxy
        # on success, reduce your resources by the amount you spent
        # and increase your product by the amount you got

class Producer(Individual):
    '''The base class for all Producers
    DATA
        have a product 
        resources consumed per unit produced
        time taken per unit produced

    ACTIONS
        ability to sell
             advertise the product in the Market 
             negotiate a deal with an agent when contacted
             finalize the transaction
    '''

    def __init__(self, name, resources, need, product, roc=None, cost=None, speed=None):
        self.product = product
        self.cost = cost
        self.speed = speed
        if not self.cost:
            self.cost = 10 # TODO(willie): randomize
        if not self.speed:
            self.speed = 1000

        super().__init__(name, resources, need, roc)


class Agent(Consumer, Producer):
    '''Class for agent in the economy. All agents are producers and consumers.

    '''

    def __init__(self, market, name, need, product, resources, roc=None, cost=None, speed=None): 
        Consumer.__init__(self, name, resources, need, roc)
        Producer.__init__(self, name, resources, need, product, roc, cost, speed)

        self.market = market


    def run(self):
        while not self.fail():
            action = choose_role()
            action()

        print("I have failed")
        print(self)

    def __str__(self):
        return \
        '''~{}~
        resources: {}

        Need: {}
        Rate of consumption: {}

        Product: {}
        Cost to make: {}
        Speed of production: {}'''.format(self.name,
                                          self.resources,
                                          self.need,
                                          self.roc,
                                          self.product,
                                          self.cost,
                                          self.speed)

