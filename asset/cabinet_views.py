#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'

import  models


model = '''<tr><td class="jgtable" align="center" height="2" valign="bottom">&nbsp;</td></tr>'''
model2 = '''<tr style="height: 2px;  font-weight: normal;">
                <td class="jgtable" align="center" rowspan="%s" >
                    <a href="/asset/asset_list/%s/" target="_blank">
                    <img src="/static/assets/img/jf/%s.gif" style="" onmouseover="displayDIV('%s'); return false" onmouseout="hiddenDIV('%s'); return false" height="auto" width="127">
                    </a>
                      <div id="%s" style="z-index:3;border-style: outset; border-color: -moz-use-text-color; border-width: 0px; background: rgb(255, 255, 255) none repeat scroll 0 0; display: none; position: absolute; width: 127px; text-align: left;">
                          <table cellpadding="3" cellspacing="1">
                              <tbody>
                              <tr>
                                  <td>name:%s<br>位置:%s<br>机型:%s U<br>状态:%s<br></td>
                              </tr>
                      </tbody>
                      </table>
                      </div>
                    </td>
                </tr>'''

def Cabinet_data():
    data = {}
    statuss = {'start':'%suup','Disable':'%sudown','Disable_down':'%sudown','maintain':'%suweixiu'}
    cabinet_list = models.Cabinet.objects.all()
    if len(cabinet_list) == 0:
        return data
    for i in cabinet_list:
        acc_list = [model, model, model, model, model, model, model, model, model, model, model, model, model, model,
                    model, model, model, model, model, model, model, model, model, model, model, model, model, model,
                    model, model, model, model, model, model, model, model, model, model, model, model, model, model,
                    model, model, model, model, model, model]

        obj = models.Asset.objects.filter(cabinet__name__exact=i)
        for item in obj:
            begin_position = item.cabinet_begin
            end_position = item.cabinet_end
            if not begin_position  and not end_position :
                continue
            elif end_position != None and begin_position != end_position:
                new_model2 = model2%(end_position - begin_position,str(item.id),statuss[item.status]%(end_position - begin_position+1),str(item.sn),str(item.sn),str(item.sn),str(item.name.encode('utf-8')),str(item.cabinet_begin)+'-'+str(item.cabinet_end),end_position - begin_position+1,item.get_status_display().encode('utf-8'))
                acc_list[-end_position] = new_model2
                data[i] = acc_list
            elif begin_position == end_position:
                new_model2 = model2 % (
                1,str(item.id), statuss[item.status] % (end_position - begin_position + 1), str(item.sn),
                str(item.sn), str(item.sn), str(item.name), str(item.cabinet_end),
                end_position - begin_position + 1, item.get_status_display().encode('utf-8'))
                acc_list[-end_position] = new_model2
                data[i] = acc_list

    return data
