"""
 mbed CMSIS-DAP debugger
 Copyright (c) 2006-2013 ARM Limited

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

from flash import Flash
import logging

flash_algo = { 'load_address' : 0x20000000,
               'instructions' : [
                                0xE00ABE00, 0x062D780D, 0x24084068, 0xD3000040, 0x1E644058, 0x1C49D1FA, 0x2A001E52, 0x4770D1F2,
                                0xb510492f, 0x60084449, 0x2100482e, 0x482f6001, 0x44484a2d, 0x22016002, 0x04926041, 0x02926082,
                                0x220560c2, 0x61420692, 0x03122201, 0x46026182, 0x70113220, 0x62411e49, 0xf929f000, 0xd0002800,
                                0xbd102001, 0x47702000, 0xb5084a21, 0x0349447a, 0x0c0a9200, 0x481d4601, 0x44482300, 0xf9b7f000,
                                0xd0002800, 0xbd082001, 0x4919b510, 0x48174479, 0x44483920, 0xf891f000, 0xd0002800, 0xbd102001,
                                0x4b13b510, 0x4601447b, 0x22014810, 0x02923b38, 0xf0004448, 0x2800f8b4, 0x2001d000, 0xb538bd10,
                                0x490b460c, 0x39584479, 0x46019100, 0x46134807, 0x44484622, 0xf948f000, 0xd0002800, 0xbd382001,
                                0x00000004, 0x40048100, 0x40020000, 0x00000008, 0x00000085, 0x4604b570, 0x25006800, 0x061b7803,
                                0x2370d5fc, 0x20007003, 0x0003e03a, 0xfa60f000, 0x0f0b070c, 0x1f1b1713, 0x2f2b2723, 0x68263633,
                                0x71f37813, 0x6826e02a, 0x71b37853, 0x6826e026, 0x71737893, 0x6826e022, 0x713378d3, 0x6826e01e,
                                0x72f37913, 0x6826e01a, 0x72b37953, 0x6826e016, 0x72737993, 0x6826e012, 0x723379d3, 0x6826e00e,
                                0x73f37a13, 0x6826e00a, 0x73b37a53, 0x6826e006, 0x73737a93, 0x6826e002, 0x73337ad3, 0xb2c01c40,
                                0xd9c24288, 0x20806821, 0xe0037008, 0x1c416a60, 0x4780d000, 0x78006820, 0xd5f70600, 0x78006820,
                                0xd5010681, 0xe0062504, 0xd50106c1, 0xe0022508, 0xd00007c0, 0x46282510, 0xb508bd70, 0x2244460b,
                                0x700a4669, 0x2100466a, 0xbd084798, 0x4614b538, 0xd002078a, 0x300120ff, 0x6843bd38, 0xd803428b,
                                0x189a6882, 0xd80d428a, 0x428a68c2, 0x6903d803, 0x428b18d3, 0x2002d801, 0x1a89bd38, 0x05d22201,
                                0xe0001889, 0x22081ac9, 0x701a466b, 0x705a0c0a, 0x709a0a0a, 0x466a70d9, 0x47a02103, 0xb5ffbd38,
                                0x4615b081, 0x27019a01, 0x26006852, 0x02bf1948, 0xd804428a, 0x689b9b01, 0x428318d3, 0x9a01d20f,
                                0x428a68d2, 0x9b01d804, 0x18d3691b, 0xd2014283, 0xe0292602, 0x21011a88, 0x184405c9, 0x1a8ce000,
                                0x46204639, 0xf907f000, 0xd0022900, 0x360126ff, 0x4639e01a, 0xf0004628, 0x2900f8fe, 0x2601d012,
                                0x2009e012, 0x70084669, 0x70480c20, 0x70880a20, 0x9b0470cc, 0x2103466a, 0x47989801, 0xd1030006,
                                0x19e41bed, 0xd1ec2d00, 0xb0054630, 0xb5f0bdf0, 0x24006801, 0x0612780a, 0x2270d5fc, 0x6802700a,
                                0x71d12103, 0x22806801, 0x6803718a, 0x71592100, 0x23fc6805, 0x6803712b, 0x680373d9, 0x6802701a,
                                0x061b7813, 0x7a55d5fc, 0x07177a12, 0x0f3f2201, 0x105603d2, 0xf000003b, 0x0910f96b, 0x09100e0b,
                                0x10090909, 0x09090e1f, 0x11090909, 0xe0056102, 0x03522203, 0x6106e7fa, 0x6101e000, 0x0f12072a,
                                0xf0000013, 0x0c10f955, 0x120f0c0c, 0x1d1b1815, 0x0c0c0c1f, 0x0d0c0c0c, 0x03522201, 0x61c1e7e6,
                                0xbdf04620, 0x02c92101, 0x2101e7f9, 0xe7f60289, 0x02492101, 0x21ffe7f3, 0xe7f03101, 0xe7ee2180,
                                0xe7ec2140, 0xe7ea2120, 0x4607b5fe, 0x461d4616, 0x198a2000, 0xd002078b, 0x300120ff, 0x07b3bdfe,
                                0x2001d001, 0x687bbdfe, 0xd803428b, 0x191c68bc, 0xd20d4294, 0x428b68fb, 0x693cd803, 0x4294191c,
                                0x2002d201, 0x2201bdfe, 0x05d21ac9, 0xe01b188c, 0xe0191acc, 0x46692006, 0x0c207008, 0x0a207048,
                                0x70cc7088, 0x710878e8, 0x714878a8, 0x71887868, 0x71c87828, 0x466a9b08, 0x46382107, 0x28004798,
                                0x1d24d1e0, 0x1d2d1f36, 0xd1e32e00, 0xb5febdfe, 0x46044615, 0x00a86842, 0x461e1840, 0xd803428a,
                                0x18d368a3, 0xd808428b, 0x428b68e3, 0x6927d803, 0x428b19db, 0x2002d801, 0x4282bdfe, 0x68a3d805,
                                0x428318d3, 0x1a8fd301, 0x68e2e00a, 0xd9034282, 0x18d36923, 0xd3ee4283, 0x21011a88, 0x184705c9,
                                0x46382104, 0xf817f000, 0xd0022900, 0x300120ff, 0x2001bdfe, 0x70084669, 0x70480c38, 0x70880a38,
                                0x0a2870cf, 0x714d7108, 0x9b08718e, 0x2106466a, 0x47984620, 0x2200bdfe, 0x428b0903, 0x0a03d32c,
                                0xd311428b, 0x469c2300, 0x4603e04e, 0xd43c430b, 0x08432200, 0xd331428b, 0x428b0903, 0x0a03d31c,
                                0xd301428b, 0xe03f4694, 0x428b09c3, 0x01cbd301, 0x41521ac0, 0x428b0983, 0x018bd301, 0x41521ac0,
                                0x428b0943, 0x014bd301, 0x41521ac0, 0x428b0903, 0x010bd301, 0x41521ac0, 0x428b08c3, 0x00cbd301,
                                0x41521ac0, 0x428b0883, 0x008bd301, 0x41521ac0, 0x428b0843, 0x004bd301, 0x41521ac0, 0xd2001a41,
                                0x41524601, 0x47704610, 0x0fcae05d, 0x4249d000, 0xd3001003, 0x40534240, 0x469c2200, 0x428b0903,
                                0x0a03d32d, 0xd312428b, 0x018922fc, 0x0a03ba12, 0xd30c428b, 0x11920189, 0xd308428b, 0x11920189,
                                0xd304428b, 0xd03a0189, 0xe0001192, 0x09c30989, 0xd301428b, 0x1ac001cb, 0x09834152, 0xd301428b,
                                0x1ac0018b, 0x09434152, 0xd301428b, 0x1ac0014b, 0x09034152, 0xd301428b, 0x1ac0010b, 0x08c34152,
                                0xd301428b, 0x1ac000cb, 0x08834152, 0xd301428b, 0x1ac0008b, 0xd2d94152, 0x428b0843, 0x004bd301,
                                0x41521ac0, 0xd2001a41, 0x46634601, 0x105b4152, 0xd3014610, 0x2b004240, 0x4249d500, 0x46634770,
                                0xd300105b, 0xb5014240, 0x46c02000, 0xbd0246c0, 0x4674b430, 0x78251e64, 0x42ab1c64, 0x461dd200,
                                0x005b5d63, 0xbc3018e3, 0x00004718, 0xfffffffe
                                ],
               'pc_init' : 0x20000020,
               'pc_eraseAll' : 0x20000088,
               'pc_program_page' : 0x200000be,
               'begin_stack' : 0x20001000,
               'begin_data' : 0x20002000,
               'static_base' : 0x200005ec,
               'page_size' : 1024
              };

memoryMapXML =  "<?xml version=\"1.0\"?>" \
                "<!DOCTYPE memory-map PUBLIC \"+//IDN gnu.org//DTD GDB Memory Map V1.0//EN\" \"http://sourceware.org/gdb/gdb-memory-map.dtd\">" \
                "<memory-map>" \
                    "<memory type=\"flash\" start=\"0x0\" length=\"0x20000\"> <property name=\"blocksize\">0x400</property></memory>" \
                    "<memory type=\"ram\" start=\"0x20000000\" length=\"0x3000\"> </memory>" \
                "</memory-map>"


class Flash_kl25z(Flash):
    
    def __init__(self, target):
        Flash.__init__(self, target, flash_algo, memoryMapXML)

    def checkSecurityBits(self, address, data):
        #error if security bits have unexpected values
        if (address == 0x400):
            for i in range(12):
                logging.debug("data[%d] at add 0x%X: 0x%X", i, i, data[i])
                if (data[i] != 0xff):
                    return 0

            logging.debug("data[%d] at add 0x%X: 0x%X", i+3, i+3, data[i+3])
            logging.debug("data[%d] at add 0x%X: 0x%X", i+4, i+4, data[i+4])
            if ((data[i+3] != 0xff) or (data[i+4] != 0xff)):
                return 0

        return 1
