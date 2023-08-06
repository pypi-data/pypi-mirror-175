#  WotoPlatform-Py - A Python library for interacting with WotoPlatform API.
#  Copyright (C) 2021-2022  ALiwoto - <woto@kaizoku.cyou> <https://github.com/ALiwoto>
#
#  This file is part of WotoPlatform-Py.
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .base_types.scaffold import *
from .data_types.version_data import *
from .data_types.users_data import *
from .clientBase import *
from .permissions import  *

__all__ = [
    RawResponse,
    RawDScaffold,
    ScaffoldHolder,
    Scaffold,
    DScaffold,
    EmptyScaffoldData,
    RScaffold,
    UserPermission,
    ClientBase,
    ResultScaffold,
    VersionData,
    VersionResponse,
    VersionResult,
    LoginUserData,
    LoginUserResponse,
    LoginUserResult,
    RegisterUserData,
    RegisterUserResponse,
    RegisterUserResult,
    ChangeUserBioData,
    ChangeUserBioResponse,
    GetUserFavoriteData,
    GetUserFavoriteResponse,
    GetUserFavoriteResult,
    GetUserFavoriteCountData,
    GetUserFavoriteCountResponse,
    GetUserFavoriteCountResult,
    SetUserFavoriteData,
    SetUserFavoriteResponse,
    ResolveUsernameData,
    ResolveUsernameResponse,
    ResolveUsernameResult,
]
