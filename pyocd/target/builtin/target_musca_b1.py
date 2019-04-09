# pyOCD debugger
# Copyright (c) 2018-2019 Arm Limited
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ...flash.flash import Flash
from ...core.coresight_target import CoreSightTarget
from ...core.memory_map import (FlashRegion, RamRegion, MemoryMap)
from ...debug.svd.loader import SVDFile

FLASH_ALGO_QSPI = {
    'load_address' : 0x20000000,
    'instructions': [
    0xE00ABE00, 0x062D780D, 0x24084068, 0xD3000040, 0x1E644058, 0x1C49D1FA, 0x2A001E52, 0x4770D1F2,
    0x41f0e92d, 0x460e4605, 0x24004617, 0xf995f000, 0xb1144604, 0xe8bd2001, 0x200081f0, 0x4601e7fb, 
    0x47702000, 0x2000b510, 0xf99ff000, 0xbd102000, 0x4604b510, 0x417ff024, 0x21004608, 0xf9a0f000, 
    0xbd102000, 0x41f0e92d, 0x460e4605, 0x46a84617, 0xf858f000, 0xe0032400, 0xf8085d38, 0x1c640004, 
    0xd3f942b4, 0xf84ef000, 0xe8bd2000, 0xb57081f0, 0x460c4603, 0x2100461d, 0x5c68e006, 0x42b05c56, 
    0x1868d001, 0x1c49bd70, 0xd3f642a1, 0xe7f91918, 0x4603b530, 0x461d460c, 0xe0052100, 0x42905c68, 
    0x2001d001, 0x1c49bd30, 0xd3f742a1, 0xe7f92000, 0x9800b501, 0xbd086800, 0x9800b503, 0xbd0c6001, 
    0x4604b570, 0x46290625, 0xf7ff48fc, 0xf045fff5, 0x48fa0101, 0xfff0f7ff, 0xf7ff48f8, 0x4605ffe9, 
    0xbf00e000, 0xf7ff48f5, 0xf000ffe3, 0x28020002, 0xbd70d0f7, 0x2006b510, 0xffe2f7ff, 0xf7ff20e4, 
    0xbd10ffdf, 0xbf00b510, 0x64b0f04f, 0x48eb4621, 0xffd2f7ff, 0x0101f044, 0xf7ff48e8, 0x48e7ffcd, 
    0xffc6f7ff, 0xe0004604, 0x48e4bf00, 0xffc0f7ff, 0x0002f000, 0xd0f72802, 0x301048e0, 0xffb8f7ff, 
    0x0001f000, 0xd1df2800, 0xe92dbd10, 0xb0844dff, 0x46904683, 0x9f12469a, 0xf1b89e10, 0xd0060f00, 
    0x0001f1a8, 0x0003f000, 0x0008f040, 0x2000e000, 0xb12f9003, 0xf0001e78, 0xf0400007, 0xe0000008, 
    0x90022000, 0x1e70b12e, 0x0007f000, 0x0008f040, 0x2000e000, 0x25009001, 0x444949c9, 0x98137809, 
    0xb2c04348, 0x48c59000, 0x99051d00, 0xff84f7ff, 0xbf00b33e, 0xe0042400, 0x0004f81a, 0x2505ea40, 
    0x2e041c64, 0x4630da01, 0x2004e000, 0xd8f342a0, 0x48ba4629, 0xf7ff3018, 0x2500ff6f, 0xe0042404, 
    0x0004f81a, 0x2505ea40, 0x2e081c64, 0x4630da01, 0x2008e000, 0xd8f342a0, 0x48b04629, 0xf7ff301c, 
    0xea4fff5b, 0x9802610b, 0x5100ea41, 0xea419803, 0x98014100, 0x3100ea41, 0xf0009800, 0xea41001f, 
    0x462915c0, 0xf7ff48a5, 0xf045ff47, 0x48a30101, 0xff42f7ff, 0xf7ff48a1, 0x4605ff3b, 0x489fbf00, 
    0xff36f7ff, 0x0002f000, 0xd0f82802, 0x489bb31f, 0xf7ff3010, 0x4605ff2d, 0xe0032400, 0x55059811, 
    0x1c640a2d, 0xda012f04, 0xe0004638, 0x42a02004, 0x4892d8f4, 0xf7ff3014, 0x4605ff1b, 0xe0032404, 
    0x55059811, 0x1c640a2d, 0xda012f08, 0xe0004638, 0x42a02008, 0xb008d8f4, 0x8df0e8bd, 0xb087b500, 
    0x21032000, 0xe9cdaa05, 0x46030200, 0xe9cd4602, 0x46011002, 0xf7ff209f, 0xf89dff48, 0x28200014, 
    0xf89dd139, 0x28ba0015, 0x2000d135, 0xaa052102, 0x0200e9cd, 0x46024603, 0x1002e9cd, 0x20b54601, 
    0xff33f7ff, 0x0015f89d, 0xd103288f, 0x0014f89d, 0xd02028ff, 0xf88d208f, 0x20ff0018, 0x0019f88d, 
    0xf7ff2006, 0x2000fedd, 0xe9cd2302, 0x90023000, 0x4602ab06, 0x90034601, 0xf7ff20b1, 0xf7ffff16, 
    0x2066fef1, 0xfeccf7ff, 0xfeecf7ff, 0xf7ff2099, 0xf7fffec7, 0xb007fee7, 0xb510bd00, 0x2400b086, 
    0x21032000, 0xe9cdaa05, 0x46030200, 0xe9cd4602, 0x46011002, 0xf7ff209f, 0xf89dfef8, 0x28ba0015, 
    0x2401d000, 0xb0064620, 0xb510bd10, 0x20064604, 0xfea6f7ff, 0xf7ff20c7, 0xf7fffea3, 0xbd10fec3, 
    0xb085b530, 0x460d4604, 0xf7ff2006, 0x2000fe99, 0xe9cda904, 0x46030100, 0x46212203, 0x0502e9cd, 
    0xf7ff20d8, 0xf7fffed2, 0xb005fead, 0xb510bd30, 0xf04fbf00, 0xf7ff40a5, 0xf000fe7b, 0x28004000, 
    0xf04fd0f7, 0xf7ff40a5, 0x4604fe73, 0x1480f024, 0xf04f4621, 0xf7ff40a5, 0xbd10fe6f, 0xf04fb510, 
    0xf7ff40a5, 0x4604fe65, 0x0480f044, 0xf04f4621, 0xf7ff40a5, 0xbd10fe61, 0x45f0e92d, 0x4606b089, 
    0x4617468a, 0x4654463d, 0xe05046b0, 0xd30d2d04, 0xf88d7820, 0x78600017, 0x0016f88d, 0xf88d78a0, 
    0x78e00015, 0x0014f88d, 0xe02b1f2d, 0xd10d2d03, 0xf88d7820, 0x78600017, 0x0016f88d, 0xf88d78a0, 
    0x20ff0015, 0x0014f88d, 0xe01b2500, 0xd10c2d02, 0xf88d7820, 0x78600017, 0x0016f88d, 0xf88d20ff, 
    0xf88d0015, 0x25000014, 0x2d01e00c, 0x7820d10a, 0x0017f88d, 0xf88d20ff, 0xf88d0016, 0xf88d0015, 
    0x25000014, 0xf7ff2006, 0x2000fe1b, 0x2304aa07, 0x2001e9cd, 0x90039300, 0x2203ab05, 0x20024641, 
    0xfe53f7ff, 0xfe2ef7ff, 0x0804f108, 0x19f01d24, 0xd8ab4540, 0xb0092000, 0x85f0e8bd, 0x52800090, 
    0x00000005, 0xb088b570, 0x460c4605, 0x20004616, 0xaa062104, 0x1200e9cd, 0x2203ab04, 0x1002e9cd, 
    0x46104629, 0xfe31f7ff, 0x0018f89d, 0xf89d7020, 0x70600019, 0x001af89d, 0xf89d70a0, 0x70e0001b, 
    0xb0082000, 0x0000bd70, 0x00000000, 0x00000000, 
    ],
    
    # Function addresses
    'pc_init': 0x20000021,
    'pc_unInit': 0x2000003F,
    'pc_program_page': 0x20000065,
    'pc_erase_sector': 0x20000051,
    'pc_eraseAll': 0x20000045,

    'static_base' : 0x20000000 + 0x00000020 + 0x0000050C,
    'begin_stack' : 0x20000C00,
    'begin_data' : 0x20000000 + 0x1000,
    'page_size' : 0x100,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    'page_buffers' : [0x20001000, 0x20001100],   # Enable double buffering
    'min_program_length' : 0x100,

    # Flash information
    'flash_start': 0x00000000,
    'flash_size': 0x800000,
    'sector_sizes': (
        (0x0, 0x10000),
    )
    }

FLASH_ALGO_EFLASH = {
    'load_address' : 0x20000000,

    # Flash algorithm as a hex string
    'instructions': [
    0xE00ABE00, 0x062D780D, 0x24084068, 0xD3000040, 0x1E644058, 0x1C49D1FA, 0x2A001E52, 0x4770D1F2,
    0x20004603, 0x46014770, 0x47702000, 0x2000b510, 0xf953f000, 0xf0002001, 0x2000f950, 0xb570bd10,
    0xf0264606, 0xf5b5457f, 0xd2011f00, 0xe0022400, 0xf5a52401, 0x09291500, 0xf0004620, 0x2000fa74,
    0xe92dbd70, 0xb0894df7, 0x468a4680, 0x4b7ff028, 0x070aeb0b, 0x465d9c0b, 0xf5b5e053, 0xd2031f00,
    0x90042000, 0xe0049503, 0x90042001, 0x1000f5a5, 0x78609003, 0xf3607821, 0x78a0211f, 0x4000ea41,
    0xea4078e1, 0x90056001, 0x79217960, 0x211ff360, 0xea4179a0, 0x79e14000, 0x6001ea40, 0x7a619006,
    0xf3617a20, 0x7aa1201f, 0x4001ea40, 0xea407ae1, 0x90076001, 0x7b217b60, 0x211ff360, 0xea417ba0,
    0x7be14000, 0x6001ea40, 0x1b789008, 0xd20c2810, 0x9002a805, 0xe003260f, 0x980221ff, 0x1e765581,
    0xf1c01b78, 0x42b0000f, 0x3410d3f6, 0x0107e9dd, 0x0100e9cd, 0x09019803, 0xc80da804, 0xfa67f000,
    0x42bd3510, 0x2000d3a9, 0xe8bdb00c, 0xe92d8df0, 0xb08d4df7, 0x46884606, 0x4b7ff026, 0x0a08eb0b,
    0x465d9c0f, 0xf5b5e071, 0xd2031f00, 0x900c2000, 0xe004950b, 0x900c2001, 0x1000f5a5, 0xa80a900b,
    0xe9cda909, 0x980b1000, 0xab080901, 0x980caa07, 0xfac0f000, 0x0005ebaa, 0xd3412810, 0x78207861,
    0x201ff361, 0xea4078a1, 0x78e14001, 0x6001ea40, 0x79619003, 0xf3617920, 0x79a1201f, 0x4001ea40,
    0xea4079e1, 0x90046001, 0x7a217a60, 0x211ff360, 0xea417aa0, 0x7ae14000, 0x6001ea40, 0x7b609005,
    0xf3607b21, 0x7ba0211f, 0x4000ea41, 0xea407be1, 0x90066001, 0x98079903, 0xd10b4288, 0x98089904,
    0xd1074288, 0x98099905, 0xd1034288, 0x980a9906, 0xd0184288, 0x407ff006, 0xb0104428, 0x8df0e8bd,
    0x9002a807, 0xe00a2700, 0x5dc09802, 0x42885de1, 0xf006d004, 0x4428407f, 0xe7ee4438, 0xebaa1c7f,
    0x42b80005, 0x3410d8f0, 0x45553510, 0xeb06d38b, 0xe7e20008, 0x4df0e92d, 0x4607b088, 0x46144688,
    0x4a7ff027, 0x0008eb0a, 0xb2e19002, 0xf3614620, 0xb2e1201f, 0x4001ea40, 0x6604ea40, 0xe0264655,
    0x1f00f5b5, 0x2000d203, 0x46ab9007, 0x2001e003, 0xf5a59007, 0xa8061b00, 0xe9cda906, 0xea4f1000,
    0xab04111b, 0x9807aa03, 0xfa34f000, 0x42b09803, 0x9804d108, 0xd10542b0, 0x42b09805, 0x9806d102,
    0xd00342b0, 0xb0082001, 0x8df0e8bd, 0x98023510, 0xd3d54285, 0xe7f62000, 0x2300b508, 0x46019300,
    0x2200e008, 0x9b00e003, 0x93001c5b, 0x2a021c52, 0x1e49d3f9, 0xd1f42900, 0xb570bd08, 0xb10d4605,
    0xe0002002, 0x46042001, 0x6080f444, 0x600849fe, 0xf7ff2001, 0xf240ffe1, 0x43204044, 0xf8c149fb,
    0x20010198, 0xffd8f7ff, 0x4064f240, 0x49f64320, 0x20106008, 0xffd0f7ff, 0x5064f240, 0x49f34320,
    0x0198f8c1, 0x2098f643, 0xffc6f7ff, 0x5044f240, 0x49ed4320, 0x20c86008, 0xffbef7ff, 0x4044f240,
    0x49ea4320, 0x0198f8c1, 0xf7ff2001, 0xf444ffb5, 0x49e56080, 0x20016008, 0xffaef7ff, 0xf8c048e3,
    0x20144198, 0xffa8f7ff, 0x49df2000, 0x20146008, 0xffa2f7ff, 0xb570bd70, 0xb10d4605, 0xe0002002,
    0x46042001, 0x6080f444, 0x600849d7, 0xf7ff2001, 0x48d6ff93, 0x4198f8c0, 0xf7ff2001, 0xf444ff8d,
    0x49d16080, 0x20016008, 0xff86f7ff, 0xf8c048cf, 0x20014198, 0xff80f7ff, 0x7088f444, 0x600849ca,
    0xf7ff2001, 0xf444ff79, 0x49c8705e, 0x0198f8c1, 0xf7ff2001, 0xf444ff71, 0x49c460ef, 0x0198f8c1,
    0xf7ff2001, 0xf444ff69, 0x49c0705e, 0x0198f8c1, 0xf7ff2001, 0xf444ff61, 0x49bb7088, 0x20016008,
    0xff5af7ff, 0xf8c048b9, 0x203c4198, 0xff54f7ff, 0x0004f044, 0xf8c149b5, 0x20010198, 0xff4cf7ff,
    0x0024f044, 0xf8c149b1, 0x20100198, 0xff44f7ff, 0x7092f444, 0xf8c149ad, 0xf6430198, 0xf7ff2098,
    0xf444ff3b, 0x49a97082, 0x0198f8c1, 0xf7ff20c8, 0xf044ff33, 0x49a40004, 0x20016008, 0xff2cf7ff,
    0xf8c048a2, 0x20144198, 0xff26f7ff, 0xb570bd70, 0xb10d4605, 0xe0002002, 0x46042001, 0x6080f444,
    0x60084999, 0xf7ff2001, 0x4898ff17, 0x4198f8c0, 0xf7ff2001, 0xf444ff11, 0x49936080, 0x20016008,
    0xff0af7ff, 0xf8c04891, 0x20014198, 0xff04f7ff, 0x7088f444, 0x6008498c, 0xf7ff2001, 0xf444fefd,
    0x498a7046, 0x0198f8c1, 0xf7ff2001, 0xf444fef5, 0x498660e3, 0x0198f8c1, 0xf7ff2001, 0xf444feed,
    0x49827046, 0x0198f8c1, 0xf7ff2001, 0xf444fee5, 0x497d7088, 0x20016008, 0xfedef7ff, 0xf8c0487b,
    0x203c4198, 0xfed8f7ff, 0x0024f044, 0xf8c14977, 0x20c80198, 0xfed0f7ff, 0x7092f444, 0xf8c14973,
    0xf6430198, 0xf7ff2098, 0xf444fec7, 0x496e7082, 0x20106008, 0xfec0f7ff, 0xf8c0486c, 0x20144198,
    0xfebaf7ff, 0xb570bd70, 0x460e4605, 0x2002b10d, 0x2001e000, 0x48644604, 0x60061d00, 0x6080f444,
    0xf8c14962, 0x20010198, 0xfea6f7ff, 0x4004f240, 0x495d4320, 0x20016008, 0xfe9ef7ff, 0x4024f240,
    0x495a4320, 0x0198f8c1, 0xf7ff2010, 0xf240fe95, 0x43205024, 0x60084954, 0x2098f643, 0xfe8cf7ff,
    0x5004f240, 0x49514320, 0x0198f8c1, 0xf7ff20c8, 0xf240fe83, 0x43204004, 0xf8c1494c, 0x20010198,
    0xfe7af7ff, 0x6080f444, 0x60084947, 0xf7ff2001, 0x4846fe73, 0x4198f8c0, 0xf7ff2014, 0x2000fe6d,
    0xf8c14942, 0x20140198, 0xfe66f7ff, 0xe92dbd70, 0x46064df0, 0x4690460f, 0xf8dd469a, 0x2500b020,
    0x2002b10e, 0x2001e000, 0x48374604, 0x60071d00, 0x44284836, 0x81a0f8c0, 0x44284834, 0xa1a4f8c0,
    0x44284832, 0xb1a8f8c0, 0x44294930, 0xf8c19809, 0x200101ac, 0xfe40f7ff, 0x6080f444, 0xf8c1492b,
    0x20010198, 0xfe38f7ff, 0x4004f240, 0x49264320, 0x20016008, 0xfe30f7ff, 0x4084f240, 0x49234320,
    0x0198f8c1, 0xf7ff2010, 0xf240fe27, 0x43205084, 0x6008491d, 0xf7ff2004, 0xf240fe1f, 0x4320508c,
    0xf8c1491a, 0x200a0198, 0xfe16f7ff, 0x5084f240, 0x49154320, 0x20016008, 0xfe0ef7ff, 0x5004f240,
    0x49114320, 0x20106008, 0xfe06f7ff, 0x4004f240, 0x490e4320, 0x0198f8c1, 0xf7ff2001, 0xf444fdfd,
    0x49096080, 0x20016008, 0xfdf6f7ff, 0xf8c04807, 0x20144198, 0xfdf0f7ff, 0x49042000, 0x0198f8c1,
    0xf7ff2014, 0xe003fde9, 0x5010b198, 0x5010b000, 0x8df0e8bd, 0x4df0e92d, 0x460f4606, 0x469a4690,
    0xb020f8dd, 0x2010b10e, 0x2000e000, 0xb10e4605, 0xe0002002, 0x46042001, 0x6007482b, 0xf7ff2001,
    0xf444fdcb, 0x49296080, 0x0198f8c1, 0xf7ff2001, 0xf240fdc3, 0x4320400c, 0x1f094923, 0x20016008,
    0xfdbaf7ff, 0x401cf240, 0x49204320, 0x0198f8c1, 0xf7ff2001, 0xf240fdb1, 0x4320400c, 0x1f09491a,
    0x20016008, 0xfda8f7ff, 0x44284818, 0x01c0f8d0, 0x0000f8c8, 0x44284815, 0x01c4f8d0, 0x0000f8ca,
    0x44284812, 0x01c8f8d0, 0x0000f8cb, 0x4428480f, 0x11ccf8d0, 0x60019809, 0x6080f444, 0x1f09490a,
    0x20016008, 0xfd88f7ff, 0xf8c04808, 0x20014198, 0xfd82f7ff, 0x49052000, 0x0198f8c1, 0xf7ff2014,
    0xe8bdfd7b, 0x00008df0, 0x5010b19c, 0x5010b000, 0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x20000021,
    'pc_unInit': 0x20000027,
    'pc_program_page': 0x20000063,
    'pc_erase_sector': 0x2000003f,
    'pc_eraseAll': 0x2000002d,

    'static_base' : 0x20000000 + 0x00000020 + 0x000007b0,
    'begin_stack' : 0x20000a00,
    'begin_data' : 0x20000000 + 0x1000,
    'page_size' : 0x100,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    'page_buffers' : [0x20001000, 0x20001100],   # Enable double buffering
    'min_program_length' : 0x100,

    # Flash information
    'flash_start': 0x0,
    'flash_size': 0x400000,
    'sector_sizes': (
        (0x0, 0x4000),
    )
    }

class MuscaB1(CoreSightTarget):

    memoryMap = MemoryMap(
        FlashRegion(name='neflash',     start=0x0A000000, length=0x00200000, access='rx',
                        blocksize=0x4000,
                        page_size=0x100,
                        is_boot_memory=False,
                        is_default=False,
                        algo=FLASH_ALGO_EFLASH),
        FlashRegion(name='seflash',     start=0x1A000000, length=0x00200000, access='rxs',
                        blocksize=0x4000,
                        page_size=0x100,
                        is_boot_memory=False,
                        is_default=False,
                        algo=FLASH_ALGO_EFLASH,
                        alias='neflash'),
        FlashRegion(name='nqspi',       start=0x00000000, length=0x00800000, access='rx',
                        blocksize=0x10000,
                        page_size=0x100,
                        is_boot_memory=True,
                        is_external=True,
                        algo=FLASH_ALGO_QSPI),
        FlashRegion(name='sqspi',       start=0x10000000, length=0x00800000, access='rxs',
                        blocksize=0x10000,
                        page_size=0x100,
                        is_boot_memory=True,
                        is_external=True,
                        algo=FLASH_ALGO_QSPI,
                        alias='nqspi'),
        RamRegion(  name='ncoderam',    start=0x0A400000, length=0x00080000, access='rwx'),
        RamRegion(  name='scoderam',    start=0x1A400000, length=0x00080000, access='rwxs',
                        alias='ncoderam'),
        # Due to an errata, the first 8 kB of sysram is not accessible to the debugger.
        RamRegion(  name='nsysram',     start=0x20002000, length=0x0007e000, access='rwx'),
        RamRegion(  name='ssysram',     start=0x30002000, length=0x0007e000, access='rwxs',
                        alias='nsysram'),
        )

    def __init__(self, link):
        super(MuscaB1, self).__init__(link, self.memoryMap)
        self._svd_location = SVDFile.from_builtin("Musca_B1.svd")
