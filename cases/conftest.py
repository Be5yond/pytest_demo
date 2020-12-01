import pytest

from comm import db, ding, mailer


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="environment: (test|online|preonline) default is test")

    parser.addoption(
        "--notice",
        action="store",
        default="0",
        help="""send excute result message type(0 | 1 | 2 | 3)
                0: no notice send.(default)\n
                1: dingding message.\n
                2: email notice.\n
                3: both dingding and emial message.""")


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    收集测试结果，发送测试报告
    """
    result = '.'.join([f'{k}, {len(v)}' for k,v in terminalreporter.stats.items() if k])
    options = [config.option.allure_epics, config.option.allure_features]
    opt_text = '\n'.join(map(str, options))
    content = f'AutoTest Result: \n{result}'
    notice_type = int(config.getoption('--notice'))
    if notice_type & 1:
        ding.send_msg(content)
    if notice_type & 2:
        detail = f'\n查看详细报告{ding.config.get("report", "allure_url")}\n'
        for result, reports in terminalreporter.stats.items():
            if result in ('passed, failed'):
                detail += f'{result}\n'
                detail += '\n'.join([rp.nodeid+'------'+rp.outcome for rp in reports])
        mailer.sendmail(content, content+detail)


