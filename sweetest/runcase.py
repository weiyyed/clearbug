from os import path
import os,subprocess
import time
import sys
import json

from haptest.models import Element, RunCase, TestCase as TestCase_haptest, Data, GlobalData
from sweetest.data import testsuite_format, testsuite2data, testsuite2report, testsuite_format4database
from sweetest.parse import parse
from sweetest.elements import e
from sweetest.globals import g
from sweetest.windows import w
from sweetest.testsuite import TestSuite
from sweetest.testcase import TestCase
from sweetest.utility import Excel, get_record, get_all_record, set_g_header
from sweetest.log import logger
from sweetest.report import Report
from sweetest.config import _testcase, _elements, _report

# 数据库执行用例
class Autotest4database:
    def __init__(self, run_case_obj):
        g.start_time = time.strftime("@%Y%m%d_%H%M%S", time.localtime())
        self.run_obj=run_case_obj
        self.platform_id=run_case_obj.project.platform.id
        self.platform_name=run_case_obj.project.platform.platform_name
        self.project_id = run_case_obj.project
        self.modules_name = [m.module_name for m in run_case_obj.module.all()]
        desired_caps = run_case_obj.desired_caps
        self.desired_caps=eval(desired_caps)
        self.server_url = run_case_obj.server_url
        self.runcase_name=run_case_obj.runcase_name
        self.login_url=run_case_obj.pc_login_url
        self.login_user=run_case_obj.login_user
        self.login_password=run_case_obj.login_password

        if self.desired_caps:
            desired_caps_init = {
                "noReset": True,
                "unicodeKeyboard": True,
                "newCommandTimeout": "600",
            }
            self.desired_caps.update(desired_caps_init)
        else:
            self.desired_caps = {
                'platformName': 'Desktop', 'browserName': 'Chrome'}

        self.conditions = {}
        g.project_name = self.platform_name
        if not path.exists('junit'):
            os.mkdir('junit')
        self.report_xml = path.join(
            'junit', self.runcase_name + '-' + _report + g.start_time + '.xml')
        if not path.exists('report'):
            os.mkdir('report')
            # 写方式打开report-excel
        self.report_workbook = Excel(
            path.join('report', self.runcase_name + '-' + _report + g.start_time + '.xlsx'), 'w')

        self.report_data = {}  # 测试报告详细数据

    def fliter(self, **kwargs):
        # 筛选要执行的测试用例
        self.conditions = kwargs

    # 测试套件执行
    def plan(self):
        self.code = 0  # 返回码
        # 1.解析配置文件
        try:
            e.get_elements4data(Element.objects.get_dicts(platform=self.platform_id))
        except:
            logger.exception('*** Parse config file fail ***')
            self.code = -1
            sys.exit(self.code)

        self.report = Report()
        self.report_ts = {}

        # 2.逐个执行测试套件
        for runcase_name in [self.runcase_name]:
            g.sheet_name = runcase_name
            # xml 测试报告初始化
            self.report_ts[runcase_name] = self.report.create_suite(
                g.project_name, runcase_name)
            self.report_ts[runcase_name].start()

            self.run(runcase_name)

        self.report_workbook.close()

        with open(self.report_xml, 'w', encoding='utf-8') as f:
            self.report.write(f)

        self.report.data()
    #     生成allure报告
    #     import locale
        cmd="cd {} & allure generate junit -o allure_report --clean".format(os.getcwd())
        subprocess.Popen(cmd,shell=True)
    # 用例执行
    def run(self, runcase_name):
        # 1.从数据库获取测试用例集
        try:
            # data = self.testcase_workbook.read(runcase_name)
            # testsuite = testsuite_format(data)
            testsuite=testsuite_format4database(TestCase_haptest.objects.to_testcase_dicts(RunCase.objects.get_testcases(runcase_name=runcase_name)))
            set_g_header(testsuite)
            # logger.info('Testsuite imported from Excel:\n' +
            #             json.dumps(testsuite, ensure_ascii=False, indent=4))
            logger.info('From database import testsuite success')
        except Exception as e:
            logger.exception('*** From database import testsuite fail ***')
            self.code = -1
            sys.exit(self.code)

        # 2.初始化全局对象
        try:
            g.init(self.desired_caps, self.server_url)
            g.set_driver()
            # 如果测试数据文件存在，则从该文件里读取一行数据，赋值到全局变量列表里
            # data_file = path.join(
            #     'data', g.plateform + '-' + runcase_name + '.csv')
            # if path.exists(data_file):
            #     g.var = get_record(data_file)

            g.var=Data.objects.get_data_dict(project=self.project_id)
            # data_file = path.join(
            #     'data', g.plateform + '-' + runcase_name + '-globle.txt')
            # if path.exists(data_file):
            g_data=GlobalData.objects.get_data_dict()
            g.var.update(g_data)
            g.var.update({"登录地址":self.login_url,
                          "用户":self.login_user,
                          "密码":self.login_password,})
            w.init()
        except Exception as e:
            logger.exception('*** Init global object fail ***')
            logger.exception(e)
            self.code = -1
            sys.exit(self.code)

        # 3.解析测试用例集
        try:
            parse(testsuite)
            logger.debug('testsuite has been parsed:\n' + str(testsuite))
        except :
            logger.exception('*** Parse testsuite fail ***')
            self.code = -1
            sys.exit(self.code)
            # return

        # 4.执行测试套件
        ts = TestSuite(testsuite, self.report_ts[runcase_name], self.conditions)
        ts.run()

        # 5.判断测试结果
        if self.report_ts[runcase_name].high_errors + self.report_ts[runcase_name].medium_errors + \
                self.report_ts[runcase_name].high_failures + self.report_ts[runcase_name].medium_failures:
            self.code = -1

        # 6.保存测试结果
        try:
            self.report_data[runcase_name] = testsuite2report(testsuite)
            data = testsuite2data(testsuite)
            self.report_workbook.write(data, runcase_name)
        except:
            logger.exception('*** Save the report is fail ***')

