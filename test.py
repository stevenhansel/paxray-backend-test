import unittest
from datetime import datetime

from app import countCopyPasteEvents


class TestCountCopyPasteEvents(unittest.TestCase):
    def setUp(self):
        print("\n", unittest.TestCase.id(self))

    def testNormalCase(self):
        mock = [
            {
                "timestamp": datetime.fromisoformat("2022-07-13 17:53:04.470386"),
                "eventtype": "CTRL + C",
                "userid": "5afdc668c00128b62f5136db9201953d69a4a43919684dfbef3955a570f9e2fe6d9f70e38456ec9d1065a26359e96643c7eff014be753738fd4d0db3f0a7f74f",
                "acceleratorkey": None,
                "applicationname": "outlook",
            },
            {
                "timestamp": datetime.fromisoformat("2022-07-13 17:53:08.253561"),
                "eventtype": "CTRL + V",
                "userid": "5afdc668c00128b62f5136db9201953d69a4a43919684dfbef3955a570f9e2fe6d9f70e38456ec9d1065a26359e96643c7eff014be753738fd4d0db3f0a7f74f",
                "acceleratorkey": None,
                "applicationname": "excel",
            },
            {
                "timestamp": datetime.fromisoformat("2022-07-13 17:53:12.273218"),
                "eventtype": "CTRL + X",
                "userid": "5afdc668c00128b62f5136db9201953d69a4a43919684dfbef3955a570f9e2fe6d9f70e38456ec9d1065a26359e96643c7eff014be753738fd4d0db3f0a7f74f",
                "acceleratorkey": None,
                "applicationname": "excel",
            },
            {
                "timestamp": datetime.fromisoformat("2022-07-13 17:53:15.068586"),
                "eventtype": "CTRL + V",
                "userid": "5afdc668c00128b62f5136db9201953d69a4a43919684dfbef3955a570f9e2fe6d9f70e38456ec9d1065a26359e96643c7eff014be753738fd4d0db3f0a7f74f",
                "acceleratorkey": None,
                "applicationname": "excel",
            },
            {
                "timestamp": datetime.fromisoformat("2022-07-13 17:54:12.273218"),
                "eventtype": "Left-Down",
                "userid": "5afdc668c00128b62f5136db9201953d69a4a43919684dfbef3955a570f9e2fe6d9f70e38456ec9d1065a26359e96643c7eff014be753738fd4d0db3f0a7f74f",
                "acceleratorkey": "STRG+C",
                "applicationname": "outlook",
            },
            {
                "timestamp": datetime.fromisoformat("2022-07-13 17:54:15.068586"),
                "eventtype": "CTRL + V",
                "userid": "5afdc668c00128b62f5136db9201953d69a4a43919684dfbef3955a570f9e2fe6d9f70e38456ec9d1065a26359e96643c7eff014be753738fd4d0db3f0a7f74f",
                "acceleratorkey": None,
                "applicationname": "excel",
            },
        ]

        expect = [
            {"from": "outlook", "to": "excel", "count": 2},
            {"from": "excel", "to": "excel", "count": 1},
        ]

        counts = countCopyPasteEvents(mock)
        self.assertCountEqual(expect, counts.to_dict("records"))

    def testConsecutiveCopies(self):
        mock = [
            {
                "timestamp": datetime.fromisoformat("2022-07-13 17:53:04.470386"),
                "eventtype": "CTRL + C",
                "userid": "5afdc668c00128b62f5136db9201953d69a4a43919684dfbef3955a570f9e2fe6d9f70e38456ec9d1065a26359e96643c7eff014be753738fd4d0db3f0a7f74f",
                "acceleratorkey": None,
                "applicationname": "microsoft.dynamics.nav.client",
            },
            {
                "timestamp": datetime.fromisoformat("2022-07-13 17:53:08.253561"),
                "eventtype": "CTRL + V",
                "userid": "5afdc668c00128b62f5136db9201953d69a4a43919684dfbef3955a570f9e2fe6d9f70e38456ec9d1065a26359e96643c7eff014be753738fd4d0db3f0a7f74f",
                "acceleratorkey": None,
                "applicationname": "outlook",
            },
            {
                "timestamp": datetime.fromisoformat("2022-07-13 17:53:15.068586"),
                "eventtype": "CTRL + V",
                "userid": "5afdc668c00128b62f5136db9201953d69a4a43919684dfbef3955a570f9e2fe6d9f70e38456ec9d1065a26359e96643c7eff014be753738fd4d0db3f0a7f74f",
                "acceleratorkey": None,
                "applicationname": "excel",
            },
            {
                "timestamp": datetime.fromisoformat("2022-07-13 17:54:15.068586"),
                "eventtype": "CTRL + V",
                "userid": "5afdc668c00128b62f5136db9201953d69a4a43919684dfbef3955a570f9e2fe6d9f70e38456ec9d1065a26359e96643c7eff014be753738fd4d0db3f0a7f74f",
                "acceleratorkey": None,
                "applicationname": "excel",
            },
        ]
        expect = [
            {"from": "microsoft.dynamics.nav.client", "to": "excel", "count": 1},
            {"from": "microsoft.dynamics.nav.client", "to": "outlook", "count": 1},
        ]

        counts = countCopyPasteEvents(mock)
        self.assertCountEqual(expect, counts.to_dict("records"))

    def testDifferentUsers(self):
        mock = [
            {
                "timestamp": datetime.fromisoformat("2022-07-13 17:53:04.470386"),
                "eventtype": "CTRL + C",
                "userid": "5afdc668c00128b62f5136db9201953d69a4a43919684dfbef3955a570f9e2fe6d9f70e38456ec9d1065a26359e96643c7eff014be753738fd4d0db3f0a7f74f",
                "acceleratorkey": None,
                "applicationname": "outlook",
            },
            {
                "timestamp": datetime.fromisoformat("2022-07-13 17:53:06.470386"),
                "eventtype": "CTRL + C",
                "userid": "4d5e3f06f8eea359935ce508d60b1fee87673936a7a152edddf6b50595c26d32cc75f3dc9fe657882673a2b5be94a60658d97ceb5e4e70d63672f31bb7790f38",
                "acceleratorkey": None,
                "applicationname": "outlook",
            },
            {
                "timestamp": datetime.fromisoformat("2022-07-13 17:53:08.253561"),
                "eventtype": "CTRL + V",
                "userid": "5afdc668c00128b62f5136db9201953d69a4a43919684dfbef3955a570f9e2fe6d9f70e38456ec9d1065a26359e96643c7eff014be753738fd4d0db3f0a7f74f",
                "acceleratorkey": None,
                "applicationname": "excel",
            },
            {
                "timestamp": datetime.fromisoformat("2022-07-13 17:53:10.470386"),
                "eventtype": "CTRL + V",
                "userid": "4d5e3f06f8eea359935ce508d60b1fee87673936a7a152edddf6b50595c26d32cc75f3dc9fe657882673a2b5be94a60658d97ceb5e4e70d63672f31bb7790f38",
                "acceleratorkey": None,
                "applicationname": "excel",
            },
        ]
        expect = [
            {"from": "outlook", "to": "excel", "count": 2},
        ]

        counts = countCopyPasteEvents(mock)
        self.assertCountEqual(expect, counts.to_dict("records"))

    def testCopyWithoutPasting(self):
        mock = [
            {
                "timestamp": datetime.fromisoformat("2022-07-13 17:53:04.470386"),
                "eventtype": "CTRL + C",
                "userid": "5afdc668c00128b62f5136db9201953d69a4a43919684dfbef3955a570f9e2fe6d9f70e38456ec9d1065a26359e96643c7eff014be753738fd4d0db3f0a7f74f",
                "acceleratorkey": None,
                "applicationname": "outlook",
            },
            {
                "timestamp": datetime.fromisoformat("2022-07-13 17:53:06.470386"),
                "eventtype": "CTRL + X",
                "userid": "4d5e3f06f8eea359935ce508d60b1fee87673936a7a152edddf6b50595c26d32cc75f3dc9fe657882673a2b5be94a60658d97ceb5e4e70d63672f31bb7790f38",
                "acceleratorkey": None,
                "applicationname": "excel",
            },
        ]
        expect = []

        counts = countCopyPasteEvents(mock)
        self.assertCountEqual(expect, counts.to_dict("records"))


if __name__ == "__main__":
    unittest.main()
