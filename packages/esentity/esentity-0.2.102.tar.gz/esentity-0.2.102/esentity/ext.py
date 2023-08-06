#coding: utf-8
from flask import current_app, g, request, abort
from flask_login import current_user
from itsdangerous import exc
from jinja2 import TemplateNotFound, TemplateSyntaxError
from jinja2.ext import Extension
from jinja2.nodes import List, CallBlock
from esentity.models import Page, Activity
from loguru import logger
from json import dumps, loads
import html
import math
from urllib.parse import unquote
from babel.numbers import format_decimal
import pendulum


class HtmlExtension(Extension):
    tags = set(['html'])

    def __init__(self, environment):
        super(HtmlExtension, self).__init__(environment)

    def _render(self, caller):
        rv = caller()
        return html.unescape(rv)

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        body = parser.parse_statements(['name:endhtml'], drop_needle=True)
        args = []

        return CallBlock(self.call_method("_render", args), [], [], body).set_lineno(lineno)


# class LicencesExtension(Extension):
#     tags = set(['licences'])

#     def __init__(self, environment):
#         super(LicencesExtension, self).__init__(environment)

#     def _render(self, caller):
#         pages, _ = Page.get(
#             category='collection',
#             is_active=True,
#             is_searchable=True,
#             is_redirect=False,  
#             locale=g.language, 
#             _source=['title', 'path', 'alt_title'],
#             collection_mode='CasinoLicence',
#             _count=100,
#             _sort=[
#                 {'alt_title.keyword': {'order': 'asc'}}
#             ]
#         )
#         t = current_app.jinja_env.get_template('_table-licences.html')
#         s = t.render(pages=pages)
#         return s

#     def parse(self, parser):
#         lineno = next(parser.stream).lineno

#         body = ''
#         args = []

#         return CallBlock(self.call_method("_render", args), [], [], body).set_lineno(lineno)


class CollectionsExtension(Extension):
    tags = set(['collections'])

    def __init__(self, environment):
        super(CollectionsExtension, self).__init__(environment)

    def _render(self, args, caller=None):
        logger.info('collections Args IN: {0}'.format(args))

        default = ['collections', 'CasinoSoftware', 100, None, 500, []]
        _ca = len(default)
        args = args[:_ca] + default[len(args):] + args[_ca:]

        logger.info('collections Args OUT: {0}'.format(args))

        template = args[0]
        mode = args[1]
        count = int(args[2])
        aggs_key = args[3]
        aggs_count = int(args[4])
        exclude = args[5]

        items, _ = Page.get(
            category='collection',
            is_active=True,
            is_searchable=True,
            is_redirect=False,  
            locale=g.language, 
            _source=['title', 'path', 'alt_title', 'custom_text', 'logo', 'theme_color'],
            collection_mode=mode,
            _count=count,
            _exclude=exclude,
            _sort=[
                {'alt_title.keyword': {'order': 'asc'}}
            ]
        )

        aggs = []
        if aggs_key:
            filter_list =  [ 
                {"term": {"is_active": True}},
                {"term": {"is_draft": False}},
                {"term": {"is_sandbox": False}},
                {"term": {"is_searchable": True}},
                {"term": {"is_redirect": False}},
                {"term": {"category.keyword": 'provider'}},
                {"term": {"locale.keyword": g.language}},
            ]

            _aggs = {
                aggs_key: {
                    "terms": {
                        "field": f"{aggs_key}.keyword",
                        "size": aggs_count,
                        "order": {"_count": "desc"}
                    },
                    # "aggs": {
                    #     "casinos": {
                    #         "top_hits": {
                    #             "sort": [
                    #                 {
                    #                     "rating": {
                    #                         "order": "desc"
                    #                     }
                    #                 }
                    #             ],
                    #             "_source": {
                    #                 "includes": ["title", "path", "alt_title", "rating"]
                    #             },
                    #             "size": 3
                    #         }
                    #     }                
                    # }
                }
            }

            q = {
                "query": {
                    "bool": {
                        "must": filter_list,
                    }
                },
                "aggs": _aggs,
                "size": 0,
                "_source": False,
            }

            resp = current_app.es.search(index=Page._table(), body=q, request_timeout=60, ignore=[400, 404])
            aggs = resp['aggregations'][aggs_key]['buckets']

        logger.info(aggs)

        t = current_app.jinja_env.get_template(f'_ext-{template}.html')
        s = t.render(
            items=items, 
            aggs={item['key']: item['doc_count'] for item in aggs}
        )

        return s


    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        return CallBlock(self.call_method("_render", args=[List(args)]), [], [], []).set_lineno(lineno)          


# class CollectionsExtension(Extension):
#     tags = set(['collections'])

#     def __init__(self, environment):
#         super(CollectionsExtension, self).__init__(environment)

#     def _render(self, caller):
#         pages, _ = Page.get(
#             category='collection',
#             is_active=True,
#             is_searchable=True,
#             is_redirect=False,  
#             locale=g.language, 
#             _source=['title', 'path', 'alt_title', 'custom_text', 'logo'],
#             collection_mode='CasinoSoftware',
#             _count=100,
#             _sort=[
#                 {'alt_title.keyword': {'order': 'asc'}}
#             ]
#         )
#         pages = {item.alt_title: item for item in pages}

#         # v2 (with aggs)

#         filter_list =  [ 
#             {"term": {"is_active": True}},
#             {"term": {"is_draft": False}},
#             {"term": {"is_sandbox": False}},
#             {"term": {"is_searchable": True}},
#             {"term": {"is_redirect": False}},
#             {"term": {"category.keyword": 'provider'}},
#             {"term": {"locale.keyword": g.language}},
#         ]

#         _aggs = {
#             "software": {
#                 "terms": {
#                     "field": "software.keyword",
#                     "size": 500,
#                     "order": {"_count": "desc"}
#                 },
#                 # "aggs": {
#                 #     "casinos": {
#                 #         "top_hits": {
#                 #             "sort": [
#                 #                 {
#                 #                     "rating": {
#                 #                         "order": "desc"
#                 #                     }
#                 #                 }
#                 #             ],
#                 #             "_source": {
#                 #                 "includes": ["title", "path", "alt_title", "rating"]
#                 #             },
#                 #             "size": 3
#                 #         }
#                 #     }                
#                 # }
#             }
#         }

#         q = {
#             "query": {
#                 "bool": {
#                     "must": filter_list,
#                 }
#             },
#             "aggs": _aggs,
#             "size": 0,
#             "_source": False,
#         }

#         resp = current_app.es.search(index=Page._table(), body=q, request_timeout=60, ignore=[400, 404])

#         if 'status' in resp and resp['status'] in [400, 404]:
#             return ''

#         t = current_app.jinja_env.get_template('_table-simple.html')
#         s = t.render(pages=pages, title='Software', items=resp['aggregations']['software']['buckets'])

#         return s

#     def parse(self, parser):
#         lineno = next(parser.stream).lineno

#         body = ''
#         args = []

#         return CallBlock(self.call_method("_render", args), [], [], body).set_lineno(lineno)


# class CountriesExtension(Extension):
#     tags = set(['countries'])

#     def __init__(self, environment):
#         super(CountriesExtension, self).__init__(environment)

#     def _render(self, caller):
#         pages, _ = Page.get(
#             category='collection',
#             is_active=True,
#             is_searchable=True,
#             is_redirect=False,  
#             locale=g.language, 
#             _source=['title', 'path', 'alt_title'],
#             collection_mode='CasinoCountry',
#             _count=100,
#             _sort=[
#                 {'alt_title.keyword': {'order': 'asc'}}
#             ]
#         )
#         t = current_app.jinja_env.get_template('_table-countries.html')
#         s = t.render(pages=pages)
#         return s

#     def parse(self, parser):
#         lineno = next(parser.stream).lineno

#         body = ''
#         args = []

#         return CallBlock(self.call_method("_render", args), [], [], body).set_lineno(lineno)        


# class BankingExtension(Extension):
#     tags = set(['banking'])

#     def __init__(self, environment):
#         super(BankingExtension, self).__init__(environment)

#     def _render(self, caller):
#         pages, _ = Page.get(
#             category='collection',
#             is_active=True,
#             is_searchable=True,
#             is_redirect=False,  
#             locale=g.language, 
#             _source=['title', 'path', 'alt_title', 'custom_text', 'logo'],
#             collection_mode=['CasinoBanking', 'CasinoBankingLimits'],
#             _count=100,
#             _sort=[
#                 {'alt_title.keyword': {'order': 'asc'}}
#             ]
#         )
#         pages = {item.alt_title: item for item in pages}

#         # v2 (with aggs)

#         filter_list =  [ 
#             {"term": {"is_active": True}},
#             {"term": {"is_draft": False}},
#             {"term": {"is_sandbox": False}},
#             {"term": {"is_searchable": True}},
#             {"term": {"is_redirect": False}},
#             {"term": {"category.keyword": 'provider'}},
#             {"term": {"locale.keyword": g.language}},
#         ]

#         _aggs = {
#             "deposits": {
#                 "terms": {
#                     "field": "deposits.keyword",
#                     "size": 500,
#                     "order": {"_count": "desc"}
#                 },
#                 # "aggs": {
#                 #     "casinos": {
#                 #         "top_hits": {
#                 #             "sort": [
#                 #                 {
#                 #                     "rating": {
#                 #                         "order": "desc"
#                 #                     }
#                 #                 }
#                 #             ],
#                 #             "_source": {
#                 #                 "includes": ["title", "path", "alt_title", "rating"]
#                 #             },
#                 #             "size": 3
#                 #         }
#                 #     }                
#                 # }
#             }
#         }

#         q = {
#             "query": {
#                 "bool": {
#                     "must": filter_list,
#                 }
#             },
#             "aggs": _aggs,
#             "size": 0,
#             "_source": False,
#         }

#         resp = current_app.es.search(index=Page._table(), body=q, request_timeout=60, ignore=[400, 404])

#         if 'status' in resp and resp['status'] in [400, 404]:
#             return ''

#         t = current_app.jinja_env.get_template('_table-simple.html')
#         s = t.render(pages=pages, title='Payment Method', items=resp['aggregations']['deposits']['buckets'])

#         return s

#     def parse(self, parser):
#         lineno = next(parser.stream).lineno

#         body = ''
#         args = []

#         return CallBlock(self.call_method("_render", args), [], [], body).set_lineno(lineno)  


class RatingExtension(Extension):
    tags = set(['rating'])

    def __init__(self, environment):
        super(RatingExtension, self).__init__(environment)

    def _render(self, args, caller=None):
        logger.info(f'Casinos Args IN: {args}')

        default = ['casino', True, 10, False]
        _ca = len(default)
        args = args[:_ca] + default[len(args):] + args[_ca:]

        logger.info('Casinos Args OUT: {0}'.format(args))

        service = args[0]
        has_filters = args[1]
        count = int(args[2])
        row_mode = bool(args[3])

        tags = args[4:]
        logger.info('Casinos Tags: {0}'.format(tags))

        _afields = ['software', 'licences', 'deposits', 'withdrawal', 'games']
        _aggs = {
            item: {
                "terms": {
                    "field": "{0}.keyword".format(item),
                    "size": 500,
                    "order": {"_key": "asc"}
                }
            } for item in _afields
        }

        # args: service
        pages, found, aggs, id = Page.provider_by_context(
            is_searchable=True,
            is_redirect=False,
            country=current_user.country_full,
            services=service,
            provider_tags=tags,
            _locale=g.language,
            _source = [
                "title", 
                "alias", 
                "logo", 
                "logo_white",
                "logo_small",
                "external_id", 
                "theme_color", 
                "welcome_package", 
                "welcome_package_note",
                "provider_pros",
                "services",
                "welcome_package_max_bonus",
                "welcome_package_fs",
                "default_currency",
                "rating",
                "rank",
                "user_rating",
                "is_sponsored",
                "website",
                "provider_pros",
                "licences",
                "ref_link",
                "geo",
            ] + _afields, 
            _count=count,
            _aggs = _aggs
        )
        if id and has_filters:
            _c = dumps(aggs)
            current_app.redis.hset('aggs', id, _c)
            logger.info('Cache aggs {0}: {1}'.format(id, len(_c)))

        deposits_primary = ['Visa', 'Trustly', 'PayPal', 'Skrill', 'Neteller']

        t = current_app.jinja_env.get_template('_ext-rating_casinos.html')
        s = t.render(
            pages=pages, 
            has_filters=has_filters, 
            found=found, 
            service=service, 
            id=id, 
            count=count,
            tags=tags,
            deposits_primary=deposits_primary,
            row_mode=row_mode
        )
        return s

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        return CallBlock(self.call_method("_render", args=[List(args)]), [], [], []).set_lineno(lineno)          


class TopSlotsExtension(Extension):
    tags = set(['top_slots'])

    def __init__(self, environment):
        super(TopSlotsExtension, self).__init__(environment)

    def _render(self, args, caller=None):
        logger.info('Top Slots IN Args: {0}'.format(args))

        default = ['NetEnt', 8, 4, False, True]
        args = args[:4] + default[len(args):] + args[4:]

        logger.info('Top Slots OUT Args: {0}'.format(args))

        provider = args[0]
        count = int(args[1])
        in_row = int(args[2])
        random = bool(args[3])
        show_provider = bool(args[4])

        # args: service
        slots, found = Page.get(
            is_active=True, 
            is_searchable=True, 
            is_redirect=False,
            locale=g.language, 
            _source=True, 
            _count=count,
            _random=random,
            category='slot',
            software=provider, 
        )

        t = current_app.jinja_env.get_template('_ext-slots_list.html')
        s = t.render(
            slots=slots,
            in_row=in_row,
            show_provider=show_provider,
        )
        return s

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        return CallBlock(self.call_method("_render", args=[List(args)]), [], [], []).set_lineno(lineno)          


class GuideExtension(Extension):
    tags = set(['guides'])

    def __init__(self, environment):
        super(GuideExtension, self).__init__(environment)

    def _render(self, args, caller=None):
        logger.info('Guide args: {0}'.format(args))

        guides, found = Page.get(
            is_active=True, 
            is_searchable=True, 
            is_redirect=False, 
            tags=args[0],
            locale=g.language, 
            _source=['path', 'title'], 
            _count=500,
            _sort=[
                {'publishedon': {'order': 'desc'}}
            ]
        )
        t = current_app.jinja_env.get_template('_table-guides.html')
        s = t.render(pages=guides, found=found)
        return s

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        return CallBlock(self.call_method("_render", args=[List(args)]), [], [], []).set_lineno(lineno)          


class TopCasinosExtension(Extension):
    tags = set(['top_casinos'])

    def __init__(self, environment):
        super(TopCasinosExtension, self).__init__(environment)

    def _render(self, caller=None):
        top, found = Page.provider_by_context(
            country=current_user.country_full,
            is_searchable=True,
            is_redirect=False,
            _locale=g.language,
            _source = [
                "title", 
                "alias", 
                "logo", 
                "logo_white",
                "logo_small",
                "external_id", 
                "theme_color", 
                "welcome_package", 
                "welcome_package_note",
                "provider_pros",
                "services",
                "welcome_package_max_bonus",
                "welcome_package_fs",
                "default_currency",
                "rating",
                "rank",
                "user_rating",
                "is_sponsored",
                "website",
                "provider_pros",
                "licences",
                "ref_link",
                "geo",
            ], 
            _count=3
        )    
        t = current_app.jinja_env.get_template('_top-casinos.html')
        s = t.render(top=top, found=found)
        return s

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        body = ''
        args = []
        return CallBlock(self.call_method("_render", args), [], [], body).set_lineno(lineno)


class CasinoAppsExtension(Extension):
    tags = set(['casino_apps'])

    def __init__(self, environment):
        super(CasinoAppsExtension, self).__init__(environment)

    def _render(self, args, caller=None):
        logger.info('CasinoApps IN Args: {0}'.format(args))

        default = [True]
        args = args[:len(default)-1] + default[len(args):] + args[len(default)-1:] # TODO (-1 ??)

        logger.info('CasinoApps OUT Args: {0}'.format(args))

        t = current_app.jinja_env.get_template('_ext-casino-apps.html')
        s = t.render()
        return s

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        return CallBlock(self.call_method("_render", args=[List(args)]), [], [], []).set_lineno(lineno)          


class SlotPlayExtension(Extension):
    tags = set(['slot_play'])

    def __init__(self, environment):
        super(SlotPlayExtension, self).__init__(environment)

    def _render(self, args, caller=None):
        logger.info('SlotPlay IN Args: {0}'.format(args))

        title = args[0]
        alias = args[1]
        screen = args[2]

        t = current_app.jinja_env.get_template('_ext-slot-play.html')
        s = t.render(screen=screen, alias=alias, title=title)
        return s

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        return CallBlock(self.call_method("_render", args=[List(args)]), [], [], []).set_lineno(lineno)          


class AuthorExtension(Extension):
    tags = set(['author_badge'])

    def __init__(self, environment):
        super(AuthorExtension, self).__init__(environment)

    def _render(self, args, caller=None):
        logger.info('Author IN Args: {0}'.format(args))

        author = args[0]

        t = current_app.jinja_env.get_template('_ext-author.html')
        s = t.render(author=author)
        return s

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        return CallBlock(self.call_method("_render", args=[List(args)]), [], [], []).set_lineno(lineno)          


class TopAlexaExtension(Extension):
    tags = set(['top_alexa'])

    def __init__(self, environment):
        super(TopAlexaExtension, self).__init__(environment)

    def _render(self, caller=None):
        pages, _ = Page.get(
            category='provider',
            is_active=True,
            is_searchable=True,
            is_redirect=False,  
            locale=g.language, 
            _source=['title', 'path', 'alias', 'alt_title', 'rank_alexa', 'geo'],
            _count=30,
            _sort=[
                {'rank_alexa': {'order': 'asc'}}
            ]
        )
   
        t = current_app.jinja_env.get_template('_ext-top_alexa.html')
        s = t.render(pages=pages)
        return s

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        body = ''
        args = []
        return CallBlock(self.call_method("_render", args), [], [], body).set_lineno(lineno)


class CasinosExtension(Extension):
    tags = set(['casinos'])

    def __init__(self, environment):
        super(CasinosExtension, self).__init__(environment)

    def _render(self, args, caller=None):
        logger.info('casinos Args IN: {0}'.format(args))

        default = [10, 'casinos_top', True, False, None] # cnt, template, has_geo, has_append, sort, [tags...]
        _ca = len(default)
        args = args[:_ca] + default[len(args):] + args[_ca:]

        logger.info('casinos Args OUT: {0}'.format(args))

        count = int(args[0])
        template = args[1]
        has_geo = bool(args[2])
        has_append = bool(args[3])
        sorting = args[4]

        tags = args[len(default):]
        logger.info('casinos Tags: {0}'.format(tags))

        kwargs = {
            'is_searchable': True,
            'is_redirect': False,
            'country': current_user.country_full if has_geo else None,
            'provider_tags': tags,
            '_source': True, 
            '_count': count,
            '_sorting': sorting,
        }
        if len(current_app.config['AVAILABLE_LOCALE']) > 1:
            kwargs['locale_available'] = g.language

        pages, found = Page.provider_by_context(**kwargs)
        logger.info(f'Casinos found: {found}')

        if has_append and has_geo and found < count and tags:
            kwargs = {
                'is_searchable': True,
                'is_redirect': False,
                'country': None,
                'country': current_user.country_full if has_geo else None,
                '_source': True, 
                '_count': count - found,
                '_exclude': [casino._id for casino in pages],
            }
            if len(current_app.config['AVAILABLE_LOCALE']) > 1:
                kwargs['locale_available'] = g.language

            pages_level_2, found_level_2 = Page.provider_by_context(**kwargs)
            logger.info(f'Casinos level-2 found: {found_level_2}')
            pages += pages_level_2

        now = pendulum.now('UTC')

        s = str(args)
        try:
            t = current_app.jinja_env.get_template('_ext-{0}.html'.format(template))
            s = t.render(
                pages=pages, 
                found=found, 
                count=count,
                my=now.format('MMMM YYYY'),
            )
        except TemplateNotFound:
            pass

        return s

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        return CallBlock(self.call_method("_render", args=[List(args)]), [], [], []).set_lineno(lineno)          


class SlotsExtension(Extension):
    tags = set(['slots'])

    def __init__(self, environment):
        super(SlotsExtension, self).__init__(environment)

    def _render(self, args, caller=None):
        logger.info(f'Slots Args IN: {args}')

        default = [10, 'rating_slots', False] # cnt, template, has_filters, [tags...]
        _ca = len(default)
        args = args[:_ca] + default[len(args):] + args[_ca:]

        logger.info('Slots Args OUT: {0}'.format(args))

        count = int(args[0])
        template = args[1]
        has_filters = bool(args[2])

        tags = args[3:]
        logger.info('Slots Tags: {0}'.format(tags))

        _afields = ['software', 'volatility', 'themes', 'slot_features']
        _aggs = {
            item: {
                "terms": {
                    "field": "{0}.keyword".format(item),
                    "size": 500,
                    "order": {"_key": "asc"}
                }
            } for item in _afields
        }

        slots, found, aggs, id = Page.slots_by_context(
            is_searchable=True, 
            is_redirect=False, 
            _locale=g.language, 
            _source=[
                'alias', 
                'title', 
                'cover', 
                'software'
            ] + _afields, 
            _count=count,
            _aggs=_aggs,
        )            

        if id and has_filters:
            _c = dumps(aggs)
            current_app.redis.hset('aggs', id, _c)
            logger.info('Cache aggs {0}: {1}'.format(id, len(_c)))

        t = current_app.jinja_env.get_template('_ext-{0}.html'.format(template))
        s = t.render(
            slots=slots, 
            has_filters=has_filters, 
            found=found, 
            id=id, 
            count=count,
            tags=tags,
        )
        return s

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        return CallBlock(self.call_method("_render", args=[List(args)]), [], [], []).set_lineno(lineno)          


class TicketExtension(Extension):
    tags = set(['ticket'])

    def __init__(self, environment):
        super(TicketExtension, self).__init__(environment)

    def _render(self, caller):
        t = current_app.jinja_env.get_template('_ext-ticket.html')
        return t.render()

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        return CallBlock(self.call_method("_render", []), [], [], '').set_lineno(lineno)


class CookiesExtension(Extension):
    tags = set(['cookies'])

    def __init__(self, environment):
        super(CookiesExtension, self).__init__(environment)

    def _render(self, caller):
        t = current_app.jinja_env.get_template('_ext-cookies.html')
        return t.render()

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        return CallBlock(self.call_method("_render", []), [], [], '').set_lineno(lineno)


class PromoExtension(Extension):
    tags = set(['promo'])

    def __init__(self, environment):
        super(PromoExtension, self).__init__(environment)

    def _render(self, caller):
        t = current_app.jinja_env.get_template('_ext-promo.html')
        return t.render()

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        return CallBlock(self.call_method("_render", []), [], [], '').set_lineno(lineno)


class AuthExtension(Extension):
    tags = set(['auth'])

    def __init__(self, environment):
        super(AuthExtension, self).__init__(environment)

    def _render(self, caller):
        t = current_app.jinja_env.get_template('_ext-auth.html')
        return t.render()

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        return CallBlock(self.call_method("_render", []), [], [], '').set_lineno(lineno)


class AgeExtension(Extension):
    tags = set(['age'])

    def __init__(self, environment):
        super(AgeExtension, self).__init__(environment)

    def _render(self, caller):
        t = current_app.jinja_env.get_template('_ext-age.html')
        return t.render()

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        return CallBlock(self.call_method("_render", []), [], [], '').set_lineno(lineno)


class GeoCountriesExtension(Extension):
    tags = set(['geo_countries'])

    def __init__(self, environment):
        super(GeoCountriesExtension, self).__init__(environment)

    def _render(self, caller):
        t = current_app.jinja_env.get_template('_ext-geo_countries.html')
        countries = g.countries
        if not current_user.location_iso in [i for c, i in countries]:
            countries = [(current_user.location, current_user.location_iso)] + countries

        return t.render(countries=countries, current=current_user.location_iso)

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        return CallBlock(self.call_method("_render", []), [], [], '').set_lineno(lineno)


class CompareButtonExtension(Extension):
    tags = set(['compare_button'])

    def __init__(self, environment):
        super(CompareButtonExtension, self).__init__(environment)

    def _render(self, args, caller=None):
        logger.info('Args: {0}'.format(args))

        t = current_app.jinja_env.get_template('_ext-compare_button.html')
        s = t.render(uid=Page.get_urlsafe_string(6), alias=args[0], title=args[1], logo=args[2])
        return s

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        return CallBlock(self.call_method("_render", args=[List(args)]), [], [], []).set_lineno(lineno)          


class ComparatorExtension(Extension):
    tags = set(['comparator'])

    def __init__(self, environment):
        super(ComparatorExtension, self).__init__(environment)

    def _render(self, args, caller=None):
        logger.info('Args: {0}'.format(args))

        try:
            casinos = []
            casinos = []
            select_enable = False

            if request.cookies.get('comparator'):
                cmp_list = loads(unquote(request.cookies.get('comparator')))
                logger.info(f'Casinos for compare: {cmp_list}')

                casinos, _ = Page.get(
                    category='provider',
                    alias=[item['alias'] for item in cmp_list],
                    is_active=True,
                    is_searchable=True,
                    is_redirect=False,  
                    locale=g.language, 
                    _count=3,
                )

            if len(casinos) <= 3:
                recommended, _ = Page.provider_by_context(
                    country=current_user.country_full,
                    is_searchable=True,
                    is_redirect=False,
                    _locale=g.language,
                    _source=[
                        'alias', 
                        'title', 
                        'theme_color', 
                        'logo', 
                    ], 
                    _exclude=[casino._id for casino in casinos],
                    _count=6
                )

                def process_casino(i):
                    obj = Page({
                        'title': 'Casino ' + str(i + 1),
                        'logo': '/static/media/images/default-cover.png',
                        'theme_color': '#1b114d'
                    }, Page.get_urlsafe_string(6))
                    return obj

                if len(casinos) < 3:
                    select_enable = True

                casinos = casinos + [process_casino(i) for i in range(0, 3 - len(casinos))]

            t = current_app.jinja_env.get_template('_ext-comparator.html')
            attrs = {
                'General': [
                    'logo', 
                    'path', 
                    'establishedon',
                    'website',
                    'languages',
                    'services',
                    'licences',
                    'provider_pros',
                    'provider_cons',
                    'rating',
                    'user_rating',
                    'rank_alexa',
                    'geo',
                    'path',
                ],
                'Support': [
                    'support_languages',
                    'support_livechat',
                    'support_email',
                    'support_phone',
                    'support_worktime',
                    'logo',
                    'path',
                ],
                'Banking': [
                    'currencies',
                    'deposits',
                    'withdrawal',
                    'min_deposit',
                    'min_withdrawal',
                    # 'withdrawal_time',
                    'withdrawal_monthly',
                    'kyc_deposit',
                    'kyc_withdrawal',
                    'path',
                ],
                'Games': [
                    'games',
                    'software',
                    'games_count',
                    'path',
                ],
                'Promotions': [
                    'welcome_package',
                    'welcome_package_note',
                    'welcome_package_wager',
                    'path',
                ],
            }

            names = {
                'logo': '',
                'establishedon': 'Launched',
                'website': 'Website',
                'languages': 'Interface',
                'services': 'Services',
                'licences': 'Licences',
                'path': '',
                'provider_pros': 'Pros',
                'provider_cons': 'Cons',
                'rating': 'Editor Rating',
                'user_rating': 'Players Rating',
                'rank_alexa': 'Alexa Rank',
                'geo': 'Acceptable Countries',
                'support_languages': 'Support Languages',
                'support_livechat': 'Livechat Available',
                'support_email': 'Support E-mail',
                'support_phone': 'Support Phone',
                'support_worktime': 'Support Worktime',
                'currencies': 'Currencies',
                'deposits': 'Deposit Methods',
                'withdrawal': 'Withdrawal Methods',
                'min_deposit': 'Minimal Deposit',
                'min_withdrawal': 'Minimal Withdrawal',
                'withdrawal_time': 'Withdrawal Time',
                'withdrawal_monthly': 'Withdrawal Monthly Limit',
                'kyc_deposit': 'KYC Deposit',
                'kyc_withdrawal': 'KYC Withdrawal',
                'games': 'Games types',
                'software': 'Game Providers',
                'games_count': 'Games count',
                'welcome_package': 'Welcome Package',
                'welcome_package_note': 'Requirements',
                'welcome_package_wager': 'Wager',
            }

            s = t.render(
                casinos=casinos, 
                attrs=attrs, 
                names=names, 
                currency_geo=g.currency_geo,
                select_enable=select_enable,
                recommended=recommended
            )
            return s
        except Exception as e:
            logger.error(f'Comparator Exception: {e}')

        return ''

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        return CallBlock(self.call_method("_render", args=[List(args)]), [], [], []).set_lineno(lineno)          


class BlogExtension(Extension):
    tags = set(['blog'])

    def __init__(self, environment):
        super(BlogExtension, self).__init__(environment)

    def _render(self, args, caller=None):
        logger.info('blog Args: {0}'.format(args))

        default = [12, 3, True]
        _ca = len(default)
        args = args[:_ca] + default[len(args):] + args[_ca:]

        _cpp = int(args[0])
        _row = int(args[1])
        _paging = bool(args[2])

        page = 1
        p = request.args.get('page')
        if p:
            if p.isdigit():
                page = int(request.args.get('page'))
            else:
                abort(404)

        pages, total = Page.get(
            is_active=True,
            is_searchable=True, 
            is_redirect=False, 
            locale=g.language, 
            tags='Blog',
            _source=['path', 'title', 'publishedon', 'cover'],
            _count=_cpp,
            _offset=(page - 1) * _cpp,
            _sort=[
                {'publishedon': {'order': 'desc'}}
            ]
        )

        logger.debug('Page: {0}'.format(page))
        logger.debug('Total: {0}'.format(total))

        if (page - 1) * _cpp > total or (request.args.get('page') and page < 2):
            abort(404)

        paging = []
        if _paging:
            paging = [{'page': item, 'value': item} for item in range(1, math.ceil(total / _cpp) + 1)]

        t = current_app.jinja_env.get_template('_ext-blog.html')
        return t.render(pages=pages, paging=paging, current=page, row=_row)

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        return CallBlock(self.call_method("_render", args=[List(args)]), [], [], []).set_lineno(lineno)          


class TopPromoExtension(Extension):
    tags = set(['top_promo'])

    def __init__(self, environment):
        super(TopPromoExtension, self).__init__(environment)

    def _render(self, caller=None):
        logger.info(f'Generate (top_promo) for {current_user.country_full}')

        casinos, found = Page.provider_by_context(
            country=current_user.country_full,
            is_searchable=True,
            is_redirect=False,
            provider_tags='TopPromo',
            _locale=g.language,
            _source = [
                "title", 
                "alias", 
                "path",
            ], 
            _count=3
        )    
        t = current_app.jinja_env.get_template('_ext-promo.html')
        s = t.render(casinos=casinos, found=found)
        return s

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        body = ''
        args = []
        return CallBlock(self.call_method("_render", args), [], [], body).set_lineno(lineno)


class TabMenuExtension(Extension):
    tags = set(['tab_menu'])

    def __init__(self, environment):
        super(TabMenuExtension, self).__init__(environment)

    def _render(self, args, caller=None):
        logger.info('tab_menu Args: {0}'.format(args))

        path = str(args[0])

        _aggs = {
            item: {
                "terms": {
                    "field": "{0}.keyword".format(item),
                    "size": 500,
                    "order": {"_key": "asc"}
                }
            } for item in ['provider_tags', 'deposits', 'games']
        }

        _, _, aggs, _ = Page.provider_by_context(
            country=current_user.country_full,
            is_searchable=True,
            is_redirect=False,
            services=['casino'],
            _locale=g.language,
            _count=0,
            _aggs=_aggs
        )    

        def process_count(_items, _key):
            for item in _items:
                if item['item'] == _key:
                    return item['count']
            return None

        pages = [
            {'path': '/casino/casino-knowledge-base/essential-guide-to-live-dealer-online-casino.html', 'title': 'Live Casinos', 'count': process_count(aggs['games'], 'Live Games')},
            {'path': '/casino/established-online-casinos/', 'title': 'Big Brand Casinos', 'count': process_count(aggs['provider_tags'], 'Big')},
            {'path': '/collections/25-licensed-casinos-with-fastest-withdrawals.html', 'title': 'Fast Payout Casinos', 'count': process_count(aggs['provider_tags'], 'Sponsored')},
            {'path': '/casino/high-traffic-casinos/', 'title': 'High Traffic Casinos', 'count': 30},
            {'path': '/casino/casino-payment-methods/bitcoin-online-casinos.html', 'title': 'Bitcoin Casinos', 'count': process_count(aggs['deposits'], 'Bitcoin')},
            {'path': '/casino/casino-payment-methods/casinos-that-use-paypal.html', 'title': 'Paypal Casinos', 'count': process_count(aggs['deposits'], 'PayPal')},
        ]

        t = current_app.jinja_env.get_template('_ext-tab_menu.html')
        s = t.render(pages=pages, path=path)
        return s

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        return CallBlock(self.call_method("_render", args=[List(args)]), [], [], []).set_lineno(lineno)          


class RelatedPagesExtension(Extension):
    tags = set(['related_pages'])

    def __init__(self, environment):
        super(RelatedPagesExtension, self).__init__(environment)

    def _render(self, args, caller=None):
        logger.info(f'related_pages Args IN: {args}')

        default = ['RelatedBlog', None, 10]
        _ca = len(default)
        args = args[:_ca] + default[len(args):] + args[_ca:]

        logger.info('related_pages Args OUT: {0}'.format(args))

        tag = args[0]
        eid = args[1]
        count = int(args[2])

        pages, _ = Page.get(
            is_active=True, 
            is_searchable=True, 
            is_redirect=False, 
            tags=tag,
            locale=g.language, 
            _source=['path', 'title'], 
            _count=count,
            _exclude=[eid],
            _sort=[
                {'publishedon': {'order': 'desc'}}
            ]
        )

        t = current_app.jinja_env.get_template('_ext-related_pages.html')
        s = t.render(pages=pages)
        return s

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        return CallBlock(self.call_method("_render", args=[List(args)]), [], [], []).set_lineno(lineno)          


class ComplaintAddExtension(Extension):
    tags = set(['complaint_add'])

    def __init__(self, environment):
        super(ComplaintAddExtension, self).__init__(environment)

    def _render(self, args, caller=None):
        logger.info('complaint_add Args: {0}'.format(args))

        t = current_app.jinja_env.get_template('_ext-complaint_add.html')
        s = t.render()
        return s

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        return CallBlock(self.call_method("_render", args=[List(args)]), [], [], []).set_lineno(lineno)          


class CryptoRatesExtension(Extension):
    tags = set(['crypto_rates'])

    def __init__(self, environment):
        super(CryptoRatesExtension, self).__init__(environment)

    def _render(self, caller):
        t = current_app.jinja_env.get_template('_ext-crypto_rates.html')
        crypto_rates = {k.decode(): format_decimal(v.decode(), locale=g.language) for k, v in current_app.redis.hgetall('crypto_rates').items()}
        s = t.render(crypto_rates=crypto_rates)
        return s

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        return CallBlock(self.call_method("_render", []), [], [], '').set_lineno(lineno)


class SidebarExtension(Extension):
    tags = set(['sidebar'])

    def __init__(self, environment):
        super(SidebarExtension, self).__init__(environment)

    def _render(self, args, caller=None):
        logger.info('sidebar Args: {0}'.format(args))

        default = ['casinos', 3, 10, 'Online Casinos']
        _ca = len(default)
        args = args[:_ca] + default[len(args):] + args[_ca:]

        _service = args[0]
        _primary = int(args[1])
        _secondary = int(args[2])
        _title = args[3]

        _total = _primary + _secondary

        _items, _count = Page.provider_by_context(
            country=current_user.country_full,
            is_searchable=True,
            is_redirect=False,
            services=_service,
            _source=["title", "alias", "logo", "path", "logo_small", "ref_link", "welcome_package", "welcome_package_note"],
            _locale=g.language,
            _count=_total,
        )

        logger.info(f'We found {_count} items for sidebar')    

        t = current_app.jinja_env.get_template('_ext-sidebar.html')
        return t.render(items=_items, service=_service, primary=_primary, total=_total, title=_title)

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        return CallBlock(self.call_method("_render", args=[List(args)]), [], [], []).set_lineno(lineno)          


class PagesExtension(Extension):
    tags = set(['pages'])

    def __init__(self, environment):
        super(PagesExtension, self).__init__(environment)

    def _render(self, args, caller=None):
        logger.info(f'pages Args IN: {args}')

        default = ['page', 10]
        _ca = len(default)
        args = args[:_ca] + default[len(args):] + args[_ca:]

        logger.info('pages Args OUT: {0}'.format(args))

        category = args[0]
        count = int(args[1])

        kwargs = {}

        if 'provider' in category:
            kwargs = {
                'provider_tags': 'Bottom',
                '_sort': [{'rating': {'order': 'desc'}}]
            }
        elif 'page' in category:
            kwargs = {
                'tags': 'Blog',
                '_exclude_params': {'tags': 'Promo'},
                '_sort': [{'publishedon': {'order': 'desc'}}]
            }

        pages, found = Page.get(
            is_active=True,
            is_searchable=True,
            is_redirect=False,
            category=category,
            **kwargs,
            _source = [
                "title", 
                "alt_title",
                "path", 
            ], 
            _count=count,
        )

        t = current_app.jinja_env.get_template('_ext-pages.html')
        s = t.render(
            pages=pages, 
        )
        return s

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        return CallBlock(self.call_method("_render", args=[List(args)]), [], [], []).set_lineno(lineno)          


class PagesListExtension(Extension):
    tags = set(['pages_list'])

    def __init__(self, environment):
        super(PagesListExtension, self).__init__(environment)

    def _render(self, args, caller=None):
        logger.info(f'pages_list Args IN: {args}')

        default = [20, 4, 'pages_list', [], {'tags': 'Promo'}, None]
        _ca = len(default)
        args = args[:_ca] + default[len(args):] + args[_ca:]

        logger.info('pages_list Args OUT: {0}'.format(args))

        count = int(args[0])
        cols = int(args[1])
        template = args[2]
        tags = args[3]
        exclude = args[4]
        css = args[5]

        pages, found = Page.get(
            is_active=True,
            is_searchable=True,
            is_redirect=False,
            category=['page', 'collection'],
            tags=tags or ['Blog'],
            _exclude_params=exclude,
            _sort=[{'publishedon': {'order': 'desc'}}],
            _source = [
                "title", 
                "alt_title",
                "path", 
                "cover",
                "publishedon"
            ], 
            _count=count,
        )

        t = current_app.jinja_env.get_template(f'_ext-{template}.html')
        s = t.render(
            pages=pages, 
            cols=cols,
            css=css,
        )
        return s

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        return CallBlock(self.call_method("_render", args=[List(args)]), [], [], []).set_lineno(lineno)          


# class PromoPagesExtension(Extension):
#     tags = set(['promo_pages'])

#     def __init__(self, environment):
#         super(PromoPagesExtension, self).__init__(environment)

#     def _render(self, caller):
#         t = current_app.jinja_env.get_template('_ext-promo_pages.html')
#         s = t.render()
#         return s

#     def parse(self, parser):
#         lineno = next(parser.stream).lineno
#         return CallBlock(self.call_method("_render", []), [], [], '').set_lineno(lineno)


# class TocExtension(Extension):
#     tags = set(['toc'])

#     def __init__(self, environment):
#         super(TocExtension, self).__init__(environment)

#     def _render(self, caller):
#         rv = caller()

#         def parse_item(s):
#             v, k = s.split('#')
#             return {'anchor': f'#{k}', 'title': v}

#         items = [parse_item(item) for item in rv.strip().split(';')]

#         t = current_app.jinja_env.get_template('_ext-toc.html')
#         s = t.render(items=items)

#         return s

#     def parse(self, parser):
#         lineno = next(parser.stream).lineno

#         body = parser.parse_statements(['name:endtoc'], drop_needle=True)
#         args = []

#         return CallBlock(self.call_method("_render", args), [], [], body).set_lineno(lineno)


class UIExtension(Extension):
    tags = set(['ui'])

    def __init__(self, environment):
        super(UIExtension, self).__init__(environment)

    def _render(self, args, caller):
        logger.info(f'ui Args IN: {args}')

        default = ['features', False]
        _ca = len(default)
        args = args[:_ca] + default[len(args):] + args[_ca:]

        logger.info('ui Args OUT: {0}'.format(args))

        template = args[0]
        parse_content = bool(args[1])

        rv = caller().strip()
        items = []

        if parse_content:
            def parse_item(s):
                k, v = s.split(':')
                return {'key': k, 'value': v}
            try:
                items = [parse_item(item) for item in rv.split('|')]
            except:
                logger.warning(f'ui extension parse error: {rv}')

        s = rv
        try:
            t = current_app.jinja_env.get_template(f'_ext-ui_{template}.html')
            s = t.render(items=items, rv=html.unescape(rv), args=args)
        except TemplateNotFound:
            pass

        return s

    def parse(self, parser):
        tag = parser.stream.__next__()

        args = []
        try:
            while parser.stream.current.type != 'block_end':
                args.append(parser.parse_expression())
                parser.stream.skip_if('comma')
        except TemplateSyntaxError:
            pass

        body = parser.parse_statements(['name:endui'], drop_needle=True)

        callback = self.call_method('_render', args=[List(args)])
        return CallBlock(callback, [], [], body).set_lineno(tag.lineno)


class ComplaintsExtension(Extension):
    tags = set(['complaints'])

    def __init__(self, environment):
        super(ComplaintsExtension, self).__init__(environment)

    def _render(self, args, caller=None):
        logger.info(f'ComplaintsExtension Args IN: {args}')

        default = [10]
        _ca = len(default)
        args = args[:_ca] + default[len(args):] + args[_ca:]

        logger.info('ComplaintsExtension Args OUT: {0}'.format(args))

        count = int(args[0])

        complaints, total = Activity.get(
            activity='complaint',
            is_active=True,
            status=['opened', 'not_solved', 'solved', 'rejected'],
            _sort=[{'createdon': 'desc'}],
            _count=count,
        ) 

        casinos, _ = Page.get(
            category='provider',
            _all=True,
            _process=False,
            _count=1000,
            _source=[
                'path', 
            ]
        )
        casinos = {item['_id']: item['_source']['path'] for item in casinos}

        t = current_app.jinja_env.get_template('_ext-complaints.html')
        s = t.render(
            items=complaints, 
            cpp=count,
            total=total,
            count=count,
            percent=int((count / total) * 100) if total else 0,
            casinos=casinos,
        )
        return s

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
            parser.stream.skip_if('comma')

        return CallBlock(self.call_method("_render", args=[List(args)]), [], [], []).set_lineno(lineno)          


def process_aggs(_a, _k, _t):
    if _k in _a:
        _r = []
        for _i in _a[_k]:
            if _i['item'] in _t:
                _r.append(_i)
        _a[_k] = _r
    return _a

class RatingV2Extension(Extension):
    tags = set(['rating'])

    def __init__(self, environment):
        super(RatingV2Extension, self).__init__(environment)

    def _render(self, args, caller=None):
        logger.info(f'rating_v2 Args IN: {args}')

        default = ['casino', 10, False, ['software', 'provider_tags', 'deposits', 'games', 'licences'], 1000, []]
        _ca = len(default)
        args = args[:_ca] + default[len(args):] + args[_ca:]

        logger.info('rating_v2 Args OUT: {0}'.format(args))

        service = args[0]
        count = int(args[1])
        parse_kwargs = bool(args[2])
        aggs_fields = args[3]
        aggs_count = int(args[4])
        tags_enabled = args[5]

        tags = args[len(default):]
        logger.info('rating_v2 Casinos Tags: {0}'.format(tags))

        _aggs = {
            item: {
                "terms": {
                    "field": "{0}.keyword".format(item),
                    "size": aggs_count,
                    "order": {"_key": "asc"}
                }
            } for item in aggs_fields
        }

        # args: service
        items, total, aggs, _ = Page.provider_by_context(
            is_searchable=True,
            is_redirect=False,
            country=current_user.country_full,
            services=service,
            provider_tags=tags,
            _locale=g.language,
            _source=True,
            _count=count,
            _aggs=_aggs,
        )

        kw = {}
        if parse_kwargs:
            rv = caller()
            try:
                for s in rv.split('|'):
                    k, v = s.split(':')
                    kw[str(k)] = str(v)
            except:
                logger.warning(f'rating_v2 kwargs parse error: {rv}')

        t = current_app.jinja_env.get_template('_ext-rating_casinos.html')
        s = t.render(
            items=items, 
            total=total, 
            count=len(items),
            cpp=count,
            percent=int((count / total) * 100) if total else 0,
            service=service, 
            tags=tags,
            aggs=process_aggs(aggs, 'provider_tags', tags_enabled),
            **kw
        )
        return s

    def parse(self, parser):
        tag = parser.stream.__next__()

        args = []
        try:
            while parser.stream.current.type != 'block_end':
                args.append(parser.parse_expression())
                parser.stream.skip_if('comma')
        except TemplateSyntaxError:
            pass

        body = parser.parse_statements(['name:endrating'], drop_needle=True)

        callback = self.call_method('_render', args=[List(args)])
        return CallBlock(callback, [], [], body).set_lineno(tag.lineno)
