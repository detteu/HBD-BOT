# インストールした discord.py を読み込む
import discord
import asyncio
from discord import app_commands
import random
import datetime
import time
from datetime import datetime as dt
from server import keep_alive
import os
import pytz


shooter_list = ['わかばシューター','スプラシューター','プロモデラーMG','もみじシューター','N-ZAP85','スペースシューター','プライムシューター','ボールドマーカー','スプラシューターコラボ','N-ZAP89','52ガロン','L3リールガン','ボールドマーカーネオ','ジェットスイーパー','シャープマーカー','96ガロン','プロモデラーRG','L3リールガンD','ボトルガイザー','プライムシューターコラボ','ジェットスイーパーカスタム','シャープマーカーネオ','96ガロンデコ','H3リールガン']
charger_list = ['スプラチャージャー','スクイックリンα','スプラチャージャーコラボ','スプラスコープ','R-PEN/5H','スプラスコープコラボ','リッター4K','14式竹筒銃・甲','ソイチューバー','4Kスコープ']
blaster_list = ['ホットブラスター','ラピッドブラスター','ラピッドブラスターデコ','ロングブラスター','ノヴァブラスター','クラッシュブラスター','ノヴァブラスターネオ','クラッシュブラスターネオ','Rブラスターエリート']
roller_list = ['スプラローラー','カーボンローラー','スプラローラーコラボ','ダイナモローラー','ワイドローラー','ヴァリアブルローラー','カーボンローラーデコ']
fude_list = ['ホクサイ','パブロ','パブロ・ヒュー']
Slosher_list = ['バケットスロッシャー','ヒッセン','バケットスロッシャーデコ','スクリュースロッシャー','ヒッセン・ヒュー','オーバーフロッシャー','エクスプロッシャー']
spinner_list = ['バレルスピナー','スプラスピナー','ハイドラント','スプラスピナーコラボ','ノーチラス47','クーゲルシュライバー']
Maneuvers_list = ['スプラマニューバー','デュアルスイーパー','スパッタリー','クアッドホッパーブラック','ケルビン525','スパッタリー・ヒュー']
shelter_list = ['パラシェルター','キャンピングシェルター','スパイガジェット']
wiper_list = ['ドライブワイパー','ジムワイパー']
stringer_list = ['トライストリンガー','LACT450']
no_kill_list = ['スペースシューター','パブロ','パブロヒュー','RH−5PEN','竹','銀モデ','金モデ','L3リールガン','ワイドローラー','スパイガジェット','クラッシュブラスター','クラッシュブラスターネオ']
user_name = []

no = [':zero:',':one:',':two:',':three:',':four:',':five:',':six:',':seven:',':eight:',':nine:',':keycap_ten:']
no_uc = ['0️⃣','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
d_flg = 0

#=============スプレッドシートログイン設定開始===============================
import gspread
#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 
#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('spreadsheet-test-383500-ed5149b64893.json', scopes=scope)
#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)
#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = '10bOBDnNqqiEk2OVyQ-2woXUgjnWI9QUEH212zTQivJM'
#共有設定したスプレッドシートを開く
workbook = gc.open_by_key(SPREADSHEET_KEY)
#=============スプレッドシートログイン設定終了===============================

#=======ボタンの設定===================
#Entryボタンの設定
class EntryButton(discord.ui.View): # UIキットを利用するためにdiscord.ui.Viewを継承する
    def __init__(self, timeout=180): # Viewにはtimeoutがあり、初期値は180(s)である
        super().__init__(timeout=timeout)
      
    @discord.ui.button(label="参加登録", style=discord.ButtonStyle.success, custom_id="entry_button")
    async def input(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

class EntryButton2(discord.ui.View): # UIキットを利用するためにdiscord.ui.Viewを継承する
    def __init__(self, timeout=180): # Viewにはtimeoutがあり、初期値は180(s)である
        super().__init__(timeout=timeout)
      
    @discord.ui.button(label="参加登録", style=discord.ButtonStyle.success, custom_id="entry_button2")
    async def input(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

async def on_EntryButton(interaction:discord.Interaction):
    global workbook
    #共有設定したスプレッドシートを開く
    worksheet_name = workbook.worksheet('表紙').acell('B1').value
    #共有設定したスプレッドシートを開く
    worksheet = workbook.worksheet(worksheet_name)
    #現在のチーム登録数を受け取る
    teams = int(worksheet.acell('I7').value)
    cell_list = worksheet.range(3,1,3+teams-1,1) #対戦表名を受け取る(範囲指定)
    rnd = [cell.value for cell in cell_list] #対戦表名を受け取る
    flg = False
    for ent in rnd:
        if ent == interaction.user.name:
          flg = True
    if flg == False:
        await interaction.response.send_message("参加しました",ephemeral=True)
        #セルの値にチームメイトチームメンバーを登録
        worksheet.update_cell(teams+3,1, interaction.user.name)#参加者
        worksheet.update_cell(teams+3,2, '0')#ポイント初期化
    else:
        await interaction.response.send_message("登録済みです",ephemeral=True)

async def on_EntryButton2(interaction:discord.Interaction):
  modal = team_add2_md(user= interaction.user.name)
  await interaction.response.send_modal(modal)
  

#得点ボタンの設定
class PointButton(discord.ui.View): # UIキットを利用するためにdiscord.ui.Viewを継承する
    def __init__(self, timeout=180): # Viewにはtimeoutがあり、初期値は180(s)である
        super().__init__(timeout=timeout)
      
    @discord.ui.button(label="+2", style=discord.ButtonStyle.success, custom_id="point_button_p2")
    async def p2(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="+1", style=discord.ButtonStyle.primary, custom_id="point_button_p1")
    async def p1(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass
      
    @discord.ui.button(label="-1", style=discord.ButtonStyle.danger, custom_id="point_button_m1")
    async def m1(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

async def on_point_button_p2(interaction:discord.Interaction):
  global workbook
  worksheet_name = workbook.worksheet('表紙').acell('B1').value
  worksheet = workbook.worksheet(worksheet_name) #共有設定したスプレッドシートを開く
  teams = int(worksheet.acell('I7').value) #現在のチーム登録数を受け取る
  cell_list = worksheet.range(3,1,3+teams-1,1) #対戦表名を受け取る(範囲指定)
  rnd = [cell.value for cell in cell_list] #対戦表名を受け取る
  row = 3
  for ent in rnd:
    if ent == interaction.user.name:
      break
    else:
      row = row + 1
  point = int(worksheet.cell(row,2).value) #現在のポイントを取得
  add = str(point + 2)
  await interaction.response.send_message(f'+2しました\n合計値{add}になりました',ephemeral=True)
  worksheet.update_cell(row,2, add)#ポイント加算
  dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%H:%M')
  worksheet.update_cell(row,3, dt_now)#更新時間を登録

async def on_point_button_p1(interaction:discord.Interaction):
  global workbook
  worksheet_name = workbook.worksheet('表紙').acell('B1').value
  worksheet = workbook.worksheet(worksheet_name) #共有設定したスプレッドシートを開く
  teams = int(worksheet.acell('I7').value) #現在のチーム登録数を受け取る
  cell_list = worksheet.range(3,1,3+teams-1,1) #対戦表名を受け取る(範囲指定)
  rnd = [cell.value for cell in cell_list] #対戦表名を受け取る
  row = 3
  for ent in rnd:
    if ent == interaction.user.name:
      break
    else:
      row = row + 1
  point = int(worksheet.cell(row,2).value) #現在のポイントを取得
  add = str(point + 1)
  await interaction.response.send_message(f'+1しました\n合計値{add}になりました',ephemeral=True)
  worksheet.update_cell(row,2, add)#ポイント加算
  dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%H:%M')
  worksheet.update_cell(row,3, dt_now)#更新時間を登録

async def on_point_button_m1(interaction:discord.Interaction):
  global workbook
  worksheet_name = workbook.worksheet('表紙').acell('B1').value
  worksheet = workbook.worksheet(worksheet_name) #共有設定したスプレッドシートを開く
  teams = int(worksheet.acell('I7').value) #現在のチーム登録数を受け取る
  cell_list = worksheet.range(3,1,3+teams-1,1) #対戦表名を受け取る(範囲指定)
  rnd = [cell.value for cell in cell_list] #対戦表名を受け取る
  row = 3
  for ent in rnd:
    if ent == interaction.user.name:
      break
    else:
      row = row + 1
  point = int(worksheet.cell(row,2).value) #現在のポイントを取得
  add = str(point - 1)
  await interaction.response.send_message(f'-1しました\n合計値{add}になりました',ephemeral=True)
  worksheet.update_cell(row,2, add)#ポイント加算
  dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%H:%M')
  worksheet.update_cell(row,3, dt_now)#更新時間を登録

class ChatButton(discord.ui.View): # UIキットを利用するためにdiscord.ui.Viewを継承する
    def __init__(self, members, interaction, timeout=180): # Viewにはtimeoutがあり、初期値は180(s)である
      super().__init__(timeout=timeout)
      
      for member in members:
        self.add_item(ChatButton_gen(member=member,interaction=interaction))

num = 1

class ChatButton_gen(discord.ui.Button):
  member = discord.Member
  def __init__(self,member,interaction):
    super().__init__(label=member.name,style=discord.ButtonStyle.red)
    self.member = member

  async def callback(self, interaction: discord.Interaction):
    global num
    self.num = num
    await interaction.response.send_message("裏切者に通知を送りました",ephemeral=True,delete_after=4)
    view = Resp_Button(timeout=None,interaction=interaction,num=self.num)
    await self.member.send('あなたが裏切者です',view=view)
    if(num!=2):
      num=num+1
    else:
      num=1

class Resp_Button(discord.ui.View): # UIキットを利用するためにdiscord.ui.Viewを継承する
    interaction = discord.Interaction
    def __init__(self, interaction,num, timeout=180): # Viewにはtimeoutがあり、初期値は180(s)である
      super().__init__(timeout=timeout)
      self.interaction = interaction
      self.num = num
            
    @discord.ui.button(label='返答', style=discord.ButtonStyle.success)
    async def rp(self, interaction: discord.Interaction, button: discord.ui.Button):
      await interaction.response.send_message("確認の返答をしました",delete_after=3)
      await self.interaction.channel.send(f'裏切者{self.num}が確認しました',delete_after=30)


class point_set(discord.ui.View):
  def __init__(self,args,placeholder,mim_values,max_values, timeout=180): # Viewにはtimeoutがあり、初期値は180(s)である
    super().__init__(timeout=timeout)
    self.add_item(makeList(args=args,placeholder=placeholder,mim_values=mim_values,max_values=max_values))

class makeList(discord.ui.Select):
  def __init__(self,args,placeholder='',mim_values=1,max_values=1):
    options=[]
    for item in args:
      options.append(discord.SelectOption(label=item, description=''))
    
    super().__init__(placeholder=placeholder, min_values=mim_values, max_values=max_values, options=options)

  async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'{interaction.user.name}は{self.values[0]}を選択しました')

#=========モーダルの作成=======================================================================
class team_add_md(discord.ui.Modal):
  global workbook
  def __init__(self, title: str):
    super().__init__(title=title)
    self.team_name    = discord.ui.TextInput(label="チーム名", style=discord.TextStyle.short)
    self.team_member1 = discord.ui.TextInput(label="チームメンバー1", style=discord.TextStyle.short)
    self.team_member2 = discord.ui.TextInput(label="チームメンバー2", style=discord.TextStyle.short)
    self.team_member3 = discord.ui.TextInput(label="チームメンバー3", style=discord.TextStyle.short)
    self.team_member4 = discord.ui.TextInput(label="チームメンバー4", style=discord.TextStyle.short)
    self.add_item(self.team_name)
    self.add_item(self.team_member1)
    self.add_item(self.team_member2)
    self.add_item(self.team_member3)
    self.add_item(self.team_member4)

  async def on_submit(self, interaction: discord.Interaction):
    worksheet_name = workbook.worksheet('表紙').acell('B1').value
    #共有設定したスプレッドシートを開く
    worksheet = workbook.worksheet(worksheet_name)
    #現在のチーム登録数を受け取る
    teams = int(worksheet.acell('I7').value)
    cell_list = worksheet.range(3,1,3+teams-1,1) #対戦表名を受け取る(範囲指定)
    rnd = [cell.value for cell in cell_list] #対戦表名を受け取る
    flg = False
    for ent in rnd:
      if ent == self.team_name.value:
        flg = True
    if flg == False:
      await interaction.response.send_message("チーム登録完了しました!",ephemeral=True)
      #セルの値にチームメイトチームメンバーを登録
      worksheet.update_cell(teams+3,1, self.team_name.value)#チーム名
      worksheet.update_cell(teams+3,2, self.team_member1.value)#メンバー1
      worksheet.update_cell(teams+3,3, self.team_member2.value)#メンバー2
      worksheet.update_cell(teams+3,4, self.team_member3.value)#メンバー3
      worksheet.update_cell(teams+3,5, self.team_member4.value)#メンバー4
    else:
      await interaction.response.send_message("登録済みのチーム名です",ephemeral=True)

#個人でパワー込みで募集
class team_add2_md(discord.ui.Modal):
  global workbook
  def __init__(self, user: str):
    super().__init__(title=user+'の参加申請')
    self.user = user
    self.power    = discord.ui.TextInput(label="自己申告Xパワー（計測していない人はウデマエ（SとかS+とか）を記載　エリアの最大を登録）", style=discord.TextStyle.short)
    self.txt = discord.ui.TextInput(label="備考　：日程などで伝えておきたいことや意気込みなど　自由にどうぞ", style=discord.TextStyle.long)
    self.add_item(self.power)
    self.add_item(self.txt)

  async def on_submit(self, interaction: discord.Interaction):
    worksheet_name = workbook.worksheet('表紙').acell('B1').value
    #共有設定したスプレッドシートを開く
    worksheet = workbook.worksheet(worksheet_name)
    #現在のチーム登録数を受け取る
    teams = int(worksheet.acell('I7').value) 
    worksheet.update_cell(2,2, "自称パワー")#自称Xパワー
    worksheet.update_cell(2,3, "備考")#備考
    cell_list = worksheet.range(3,1,3+teams-1,1) #対戦表名を受け取る(範囲指定)
    rnd = [cell.value for cell in cell_list] #対戦表名を受け取る
    flg = False
    c=0
    for ent in rnd:
      if ent == self.user:
        flg = True
        cnt = c
      c = c + 1
    if flg == False:
      await interaction.response.send_message("チーム登録完了しました!",ephemeral=True)
      #セルの値にチームメイトチームメンバーを登録
      worksheet.update_cell(teams+3,1, self.user)#名前
      worksheet.update_cell(teams+3,2, self.power.value)#自称Xパワー
      worksheet.update_cell(teams+3,3, self.txt.value)#備考
      
    else:
      await interaction.response.send_message("登録済みの情報を上書きしました",ephemeral=True)
      #セルの値にチームメイトチームメンバーを登録
      worksheet.update_cell(cnt+3,2, self.power.value)#自称Xパワー
      worksheet.update_cell(cnt+3,3, self.txt.value)#備考
      

class event_set_md(discord.ui.Modal):
  global workbook
  def __init__(self, title: str):
    super().__init__(title=title)
    self.event_name = discord.ui.TextInput(label="イベント名", style=discord.TextStyle.short)
    self.add_item(self.event_name)

  async def on_submit(self, interaction: discord.Interaction):
    global workbook
    worksheet_name = self.event_name.value
    workbook.worksheet('表紙').update_cell(1,2,worksheet_name) #B1にライト
    await interaction.response.send_message("イベント設定完了しました",ephemeral=True)
    worksheet_list = workbook.worksheets()     #ワークシートの一覧を取得
    exist = False
    for current in worksheet_list :
      if current.title == worksheet_name :
        exist = True        #大会用のシートがあればフラグを立てる
    if exist == False :         #大会用のシートがなければここで作成する
      source_worksheet = workbook.worksheet('テンプレート')
      w_id = workbook.id
      source_worksheet.copy_to(w_id)
      new_sheet = workbook.worksheet('テンプレート のコピー')
      new_sheet.update_title(worksheet_name)
    

class add_result(discord.ui.Modal):
  global workbook
  def __init__(self, title: str):
    super().__init__(title=title)
    self.round    = discord.ui.TextInput(label="試合のラウンド数  例：1-2　だったら1に該当する数字(半角で入力)", style=discord.TextStyle.short)
    self.number   = discord.ui.TextInput(label="試合番号　例：1-2　だったら2に該当する数字(半角で入力)", style=discord.TextStyle.short)
    self.count    = discord.ui.TextInput(label="何試合目の結果か (半角で数字のみ入力)", style=discord.TextStyle.short)
    self.team_name= discord.ui.TextInput(label="勝利チーム名", style=discord.TextStyle.short)
    self.point    = discord.ui.TextInput(label="勝利チームの獲得ポイント (半角で数字のみ入力)", style=discord.TextStyle.short)
    
    self.add_item(self.round)
    self.add_item(self.number)
    self.add_item(self.count)
    self.add_item(self.team_name)
    self.add_item(self.point)

  async def on_submit(self, interaction: discord.Interaction):
    await interaction.response.send_message("試合結果の登録中!",ephemeral=True,delete_after=5)
    #共有設定したスプレッドシートを開く
    worksheet_name = workbook.worksheet('表紙').acell('B1').value
    worksheet = workbook.worksheet(worksheet_name)
    teams = int(worksheet.acell('I7').value) #チーム登録数を受け取る
    battles = int(worksheet.acell('I5').value) #試合回数を受け取る
    bs = (teams-1)*(battles*2-1) #総試合回数
    cell_list = worksheet.range(3,12,3+bs-1,12) #対戦表名を受け取る(範囲指定)
    rnd = [cell.value for cell in cell_list] #対戦表名を受け取る
    #行の確定
    for x in range(bs) : 
      txt = self.round.value+'-'+self.number.value
      if rnd[x] == txt:
        row = 3+x
        break
    #列の確定
    mch = str(worksheet.cell(row,13).value).split(' vs ') #matchを受け取り分割する
    ad=0
    ad2=0
    if mch[0] == self.team_name.value:
      ad=0
      ad2=1
    if mch[1] == self.team_name.value:
      ad=1
      ad2=0
    if (ad+ad2)!=1:
      await interaction.response.send_message('[勝利チーム名]が該当(存在)しないチームです\nチーム名を確認してください',ephemeral=True)
      return
    win_clm = 12 + int(self.count.value)*2+ad
    loss_clm = 12 + int(self.count.value)*2+ad2
    #得点書き込み
    worksheet.update_cell(row,win_clm, self.point.value) #勝利得点描画
    worksheet.update_cell(row,loss_clm, '0') #敗北得点描画
    #得点合計を集計表に記載
    #範囲指定してセル値を取得
    cell_list = worksheet.range(row,14,row,14+((battles*2-1)*2-1))
    values = [cell.value for cell in cell_list]
    xb=0
    yb=0
    cell_list = worksheet.range(3,34,3+teams-1,34) #対戦表名を受け取る(範囲指定)
    rnd = [cell.value for cell in cell_list] #対戦表名を受け取る
    for x in range(teams) :
      if rnd[x] == mch[0]:
        row0 = 3+x
        xb=xb+1
      if rnd[x] == mch[1]:
        row1 = 3+x
        xb=xb+1
      if xb==2:
        break
    cell_list = worksheet.range(2,35,2,35+teams-1) #対戦表名を受け取る(範囲指定)
    rnd = [cell.value for cell in cell_list] #対戦表名を受け取る
    for y in range(teams) :
      if rnd[y] == mch[1]:
        clm0 = 35+y
        yb=yb+1
      if rnd[y] == mch[0]:
        clm1 = 35+y
        yb=yb+1
      if yb==2:
        break
    val0=0
    val1=0
    for z in range(((battles*2-1)*2-1)) :
      if (z%2) == 0: #偶数
        if values[z]!='':
          val0 = val0 + int(values[z])
      else: #奇数
        if values[z]!='':
          val1 = val1 + int(values[z])
    worksheet.update_cell(row0,clm0, val0)
    worksheet.update_cell(row1,clm1, val1)
    await interaction.response.send_message("試合結果の登録完了しました!",ephemeral=True)

class schedule_md(discord.ui.Modal):
  def __init__(self, title: str ,icon_url: str):
    super().__init__(title=title)
    self.icon_url = icon_url
    self.date1    = discord.ui.TextInput(label="候補日 例:4/1　や　4/1^4/5　のように設定（設定必須）", style=discord.TextStyle.short,required=True)
    self.date2    = discord.ui.TextInput(label="候補日 例:4/1　や　4/1^4/5　のように設定（設定任意）", style=discord.TextStyle.short,required=False)
    self.date3    = discord.ui.TextInput(label="候補日 例:4/1　や　4/1^4/5　のように設定（設定任意）", style=discord.TextStyle.short,required=False)
    self.date4    = discord.ui.TextInput(label="候補日 例:4/1　や　4/1^4/5　のように設定（設定任意）", style=discord.TextStyle.short,required=False)
    self.date5    = discord.ui.TextInput(label="日程調整するイベントについての説明（設定任意）", style=discord.TextStyle.long,required=False)
    self.add_item(self.date1)
    self.add_item(self.date2)
    self.add_item(self.date3)
    self.add_item(self.date4)
    self.add_item(self.date5)

  async def on_submit(self, interaction: discord.Interaction):
    global d_flg
    global no
    Candidate=[]
    d_flg=0
    cnt=0
    date_list=[self.date1.value,self.date2.value,self.date3.value,self.date4.value]
    for x in date_list:
      if x != '':
        cnt=cnt+1
    for z in range(cnt):
      ch = '^'
      if ch in date_list[z]:
        data = date_list[z].split(ch)
        for z in range(len(data)):
          data[z] = dt.strptime(str(datetime.date.today().year)+'/'+data[z], '%Y/%m/%d')
        dx=1
        while not(data[dx-1]+datetime.timedelta(days=1) == data[dx]):
          data.insert(dx,data[dx-1]+datetime.timedelta(days=1))
          dx=dx+1
        Candidate=Candidate+data
      else:
        Candidate.append(date_list[z])
    for z in range(len(Candidate)):
      if type(Candidate[z]) is str:
        Candidate[z] = dt.strptime(str(datetime.date.today().year)+'/'+Candidate[z], '%Y/%m/%d')
    # Embedを定義する
    embed = discord.Embed(title='==========日程調整==========',color=0x00ff00)
    embed.set_author(name='日程調整の鬼',icon_url=self.icon_url)
    t=''
    for z in range(len(Candidate)):
      t=t+no[z]+"{0:%m/%d(%A)}".format(Candidate[z])+'\n'
    d_flg = len(Candidate)
    embed.add_field(name=self.date5.value+'\n用事がない日付のスタンプを押してください',value=t,inline=False)
    await interaction.response.send_message(embed=embed)

#=======ボットの設定======================
class BotTask:
  "ネットワーク接続が切れたときの再接続対応クラス"
  def __init__(self):
    # 再接続を行った回数
    self.retry_count = 0

  def start_with_retry(self):
    "再接続対応でBotを開始する"
    while True:
      try:
        # Botを開始する
        self._start()
        # 正常終了の時はスクリプトを終了する
        break
      except Exception as e:
        self.retry_count += 1
        print(e)
        # エラーが発生したときは
        print("retry %d" % self.retry_count)
        # 2のリトライ回数乗×5秒待つ
        interval = 5*2**self.retry_count
        print("interval %d" % interval)
        # 待ち時間が4時間超えたら、スクリプトを終了する
        if interval >= 4*60*60:
          break
        time.sleep(interval)

  def _start(self):
    # クライアントを作成
    client = self._make_client()
    # 環境変数からトークンを得る
    TOKEN = os.environ['TOKEN']
    # Botを実行
    client.run(TOKEN, reconnect=False)

  def _make_client(self):
    "Discordのクライアントを作成する"
    # リアクション削除の取得に必要
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    # Clientクラス内部で作られるイベントループは1スレッド1つ。
    # そしてエラーになると、それが閉じられるので、毎回新しく作成する
    loop = asyncio.new_event_loop()
    # それをクライアント作成時に渡す
    ct = discord.Client(intents=intents, loop=loop)
    tree = app_commands.CommandTree(ct)

    @ct.event
    # 起動時に動作する処理
    async def on_ready():
      # 接続出来たのでretry_countを戻す
      self.retry_count = 0
      # 起動したらターミナルにログイン通知が表示される
      print('We have logged in as {0.user}'.format(ct))
      print('ログインしました')
    
    @ct.event
    async def setup_hook():
      await tree.sync()

    @ct.event
    # メッセージ受信時に動作する処理
    async def on_message(message):
      global user_name
      global shooter_list
      global charger_list
      global blaster_list
      global roller_list 
      global fude_list 
      global Slosher_list 
      global spinner_list 
      global Maneuvers_list 
      global shelter_list
      global wiper_list
      global stringer_list
      global d_flg
      global no
      global no_uc
      global workbook
      global worksheet_name
      global u1
      global u2
      global mes
      wepon_list = []
      split_text = message.content.split()
      # メッセージ送信者がBotだった場合は無視する
      if message.author.bot:
        if d_flg != 0:
          for z in range(d_flg):
            await message.add_reaction(no_uc[z])
          d_flg = 0
        return
      # 発言監視用
      print(f'Message from {message.author}: {message.content}')
      # 「ランダム」と発言したら武器のランダム選択================================================
      if split_text[0] == 'ランダム':
        #list生成
        if len(split_text) != 1:
          for z in range(len(split_text)-1):
            if split_text[z+1] == 'シューター':
              wepon_list=wepon_list+shooter_list
            if split_text[z+1] == 'ローラー':
              wepon_list=wepon_list+roller_list
            if split_text[z+1] == 'チャージャー':
              wepon_list=wepon_list+charger_list
            if split_text[z+1] == 'ブラスター':
              wepon_list=wepon_list+blaster_list
            if split_text[z+1] == 'スロッシャー':
              wepon_list=wepon_list+Slosher_list
            if split_text[z+1] == 'スピナー':
              wepon_list=wepon_list+spinner_list
            if split_text[z+1] == 'マニューバー':
              wepon_list=wepon_list+Maneuvers_list
            if split_text[z+1] == 'シェルター':
              wepon_list=wepon_list+shelter_list
            if split_text[z+1] == 'ワイパー':
              wepon_list=wepon_list+wiper_list
            if split_text[z+1] == 'ストリンガー':
              wepon_list=wepon_list+stringer_list
            if split_text[z+1] == 'フデ':
              wepon_list=wepon_list+fude_list
            if split_text[z+1] == 'キル力無し':
              wepon_list=wepon_list+no_kill_list
        else:
            wepon_list=shooter_list+charger_list+blaster_list+roller_list+fude_list+Slosher_list+spinner_list+Maneuvers_list+shelter_list+wiper_list+stringer_list
    
        t='\n'
        user_name = [member.name for member in message.author.voice.channel.members]
        # Embedを定義する
        embed = discord.Embed(color=0x00ff00)
        embed.set_author(name='ランダムの魔人',icon_url=ct.user.avatar.url)
        for x in user_name:
          t = t+x+':'+wepon_list[random.randrange(len(wepon_list))]+'\n'
        embed.add_field(name='-------ランダム生成---------',value=t,inline=False)
        await message.channel.send(embed=embed)
      #「日程調整」と発言したら日程の多数決をとる==================================================
      if split_text[0] == '日程調整':
        Candidate=[]
        if len(split_text) == 1:
          await message.channel.send('日程調整の候補日を入力してください　　例：日程調整　4/1^4/5')
        for z in range(len(split_text)-1):
          ch = '^'
          if ch in split_text[z+1]:
            data = split_text[z+1].split(ch)
            for z in range(len(data)):
              data[z] = dt.strptime(str(datetime.date.today().year)+'/'+data[z], '%Y/%m/%d')
            dx=1
            while not(data[dx-1]+datetime.timedelta(days=1) == data[dx]):
              data.insert(dx,data[dx-1]+datetime.timedelta(days=1))
              dx=dx+1
            Candidate=Candidate+data
          else:
            Candidate.append(split_text[z+1])
        for z in range(len(Candidate)):
          if type(Candidate[z]) is str:
            Candidate[z] = dt.strptime(str(datetime.date.today().year)+'/'+Candidate[z], '%Y/%m/%d')
        # Embedを定義する
        embed = discord.Embed(title='==========日程調整==========',color=0x00ff00) #緑
        embed.set_author(name='日程調整の鬼',icon_url=ct.user.avatar.url)
        t=''
        for z in range(len(Candidate)):
          t=t+no[z]+"{0:%m/%d(%A)}".format(Candidate[z])+'\n'
        d_flg = len(Candidate)
        embed.add_field(name='日程調整を行います。用事がない日付のスタンプを押してください',value=t,inline=False)
        await message.channel.send(embed=embed)
      # 「イベント設定」と発言したらイベントを設定する================================================
      if split_text[0] == 'イベント設定':
        if len(split_text)!=2:
          await message.channel.send('大会設定　[大会名]\n設定形式エラーです。上記の形式で設定してください')
          return
        worksheet_name = str(split_text[1])
        workbook.worksheet('表紙').update_cell(1,2,worksheet_name) #B1にライト
        worksheet_list = workbook.worksheets()     #ワークシートの一覧を取得
        exist = False
        for current in worksheet_list :
          if current.title == worksheet_name :
            exist = True        #大会用のシートがあればフラグを立てる
        if exist == False :         #大会用のシートがなければここで作成する
          source_worksheet = workbook.worksheet('テンプレート')
          w_id = workbook.id
          source_worksheet.copy_to(w_id)
          new_sheet = workbook.worksheet('テンプレート のコピー')
          new_sheet.update_title(worksheet_name)
        await message.channel.send('現在のイベント名を'+worksheet_name+'に設定しました')
      # 「チーム登録」と発言したら総当たり戦のチーム登録================================================
      if split_text[0] == 'チーム登録':
        worksheet_name = workbook.worksheet('表紙').acell('B1').value
        if len(split_text)!=6:
          await message.channel.send('チーム登録　[チーム名] [メンバー1] [メンバー2] [メンバー3] [メンバー4]\n登録形式エラーです。上記の形式で登録してください')
          return
        #共有設定したスプレッドシートを開く
        worksheet = workbook.worksheet(worksheet_name)
        #現在のチーム登録数を受け取る
        teams = int(worksheet.acell('I7').value)
        #セルの値にチームメイトチームメンバーを登録
        worksheet.update_cell(teams+3,1, split_text[1])#チーム名
        worksheet.update_cell(teams+3,2, split_text[2])#メンバー1
        worksheet.update_cell(teams+3,3, split_text[3])#メンバー2
        worksheet.update_cell(teams+3,4, split_text[4])#メンバー3
        worksheet.update_cell(teams+3,5, split_text[5])#メンバー4
        await message.channel.send('チーム登録完了しました')
      # 「得点」と発言したら武器のランダム選択================================================
      if split_text[0] == '得点':
        if len(split_text)!=4:
          await message.channel.send('得点　[ラウンド番号] [勝利チーム名] [勝利時得点]\n登録形式エラーです。上記の形式で登録してください')
          return
        data = split_text[1].split('-')
        if len(data)!=3:
          await message.channel.send('[ラウンド番号]は1-1-1のように表記してください\n注意点：ハイフンの形式が違うと登録できないかもしれません')
          return
        #共有設定したスプレッドシートを開く
        worksheet_name = workbook.worksheet('表紙').acell('B1').value
        worksheet = workbook.worksheet(worksheet_name)
        teams = int(worksheet.acell('I7').value) #チーム登録数を受け取る
        battles = int(worksheet.acell('I5').value) #試合回数を受け取る
        bs = (teams-1)*(battles*2-1) #総試合回数
        cell_list = worksheet.range(3,12,3+bs-1,12) #対戦表名を受け取る(範囲指定)
        rnd = [cell.value for cell in cell_list] #対戦表名を受け取る
        #行の確定
        for x in range(bs) : 
          txt = data[0]+'-'+data[1]
          if rnd[x] == txt:
            row = 3+x
            break
        #列の確定
        mch = str(worksheet.cell(row,13).value).split(' vs ') #matchを受け取り分割する
        ad=0
        ad2=0
        if mch[0] == split_text[2]:
          ad=0
          ad2=1
        if mch[1] == split_text[2]:
          ad=1
          ad2=0
        if (ad+ad2)!=1:
          await message.channel.send('[勝利チーム名]が該当(存在)しないチームです\nチーム名を確認してください')
          return
        win_clm = 12 + int(data[2])*2+ad
        loss_clm = 12 + int(data[2])*2+ad2
        #得点書き込み
        worksheet.update_cell(row,win_clm, split_text[3]) #勝利得点描画
        worksheet.update_cell(row,loss_clm, '0') #敗北得点描画
        #得点合計を集計表に記載
        #範囲指定してセル値を取得
        cell_list = worksheet.range(row,14,row,14+((battles*2-1)*2-1))
        values = [cell.value for cell in cell_list]
        xb=0
        yb=0
        cell_list = worksheet.range(3,34,3+teams-1,34) #対戦表名を受け取る(範囲指定)
        rnd = [cell.value for cell in cell_list] #対戦表名を受け取る
        for x in range(teams) :
          if rnd[x] == mch[0]:
            row0 = 3+x
            xb=xb+1
          if rnd[x] == mch[1]:
            row1 = 3+x
            xb=xb+1
          if xb==2:
            break
        cell_list = worksheet.range(2,35,2,35+teams-1) #対戦表名を受け取る(範囲指定)
        rnd = [cell.value for cell in cell_list] #対戦表名を受け取る
        for y in range(teams) :
          if rnd[y] == mch[1]:
            clm0 = 35+y
            yb=yb+1
          if rnd[y] == mch[0]:
            clm1 = 35+y
            yb=yb+1
          if yb==2:
            break
        val0=0
        val1=0
        for z in range(((battles*2-1)*2-1)) :
          if (z%2) == 0: #偶数
            if values[z]!='':
              val0 = val0 + int(values[z])
          else: #奇数
            if values[z]!='':
              val1 = val1 + int(values[z])
        worksheet.update_cell(row0,clm0, val0)
        worksheet.update_cell(row1,clm1, val1)
        await message.channel.send('得点登録完了しました')
        #「イベント参加」と発言したらボタンを表示する====================================================
      if split_text[0] == 'イベント参加':
        view = EntryButton(timeout=None)
        embed = discord.Embed(color=0xff0000) #赤
        embed.set_author(name='イベント管理人',icon_url=ct.user.avatar.url)
        embed.add_field(name='==========イベント参加登録==========',value='イベントに参加希望の方はボタンを押してください',inline=False)
        await message.channel.send(embed=embed,view=view)
      #「ポイント登録」と発言したらボタンを表示する====================================================
      if split_text[0] == 'ポイント登録':
        view = PointButton(timeout=None)
        embed = discord.Embed(color=0x0000ff) #青
        embed.set_author(name='イベント得点の番人',icon_url=ct.user.avatar.url)
        embed.add_field(name='==========得点登録==========',value='試合結果に対応したポイントボタンを押してください',inline=False)
        await message.channel.send(embed=embed,view=view)    
      #「おわり」と発言したらボットを止める====================================================
      if split_text[0] == 'おわり':
        print('ログアウトしました')
        exit()
    
    @tree.command(name="event_set",description="イベント設定コマンドです。")
    async def event_set_command(interaction: discord.Interaction):
      modal = event_set_md(title='イベント設定')
      await interaction.response.send_modal(modal)
    
    @tree.command(name="schedule",description="日程調整フォームを開くためのコマンドです。")
    async def schedule_command(interaction: discord.Interaction):
      modal = schedule_md(title='日程調整フォーム',icon_url=ct.user.avatar.url)
      await interaction.response.send_modal(modal)
    
    @tree.command(name="team_add",description="イベントのチーム参加フォームを開くためのコマンドです。")
    async def team_add_command(interaction: discord.Interaction):
      modal = team_add_md(title='チーム登録フォーム')
      await interaction.response.send_modal(modal)
    
    @tree.command(name="result_add",description="イベントの試合結果登録フォームを開くためのコマンドです。")
    async def result_add_command(interaction: discord.Interaction):
      modal = add_result(title='試合結果登録フォーム')
      await interaction.response.send_modal(modal)
    
    @tree.command(name="point_set",description="個人専用の得点加減用ボタン設置コマンドです。")
    async def point_set_command(interaction: discord.Interaction):
      view = PointButton(timeout=None)
      embed = discord.Embed(color=0x0000ff)
      embed.set_author(name='イベント得点の番人',icon_url=ct.user.avatar.url)
      embed.add_field(name='==========得点登録==========',value='試合結果に対応したポイントボタンを押してください',inline=False)
      await interaction.response.send_message(embed=embed,view=view)
    
    @tree.command(name="event_add",description="イベント参加コマンドです。")
    async def event_add_command(interaction: discord.Interaction):
      view = EntryButton(timeout=None)
      embed = discord.Embed(color=0xff0000)
      embed.set_author(name='イベント管理人',icon_url=ct.user.avatar.url)
      embed.add_field(name='==========イベント参加登録==========',value='イベントに参加希望の方はボタンを押してください',inline=False)
      await interaction.response.send_message(embed=embed,view=view)
    
    @tree.command(name="event_add_power",description="イベント参加コマンドです。(個人のXPパワーを考慮したイベント用)")
    async def event_add_command2(interaction: discord.Interaction):
      view = EntryButton2(timeout=None)
      embed = discord.Embed(color=0xff0000)
      embed.set_author(name='イベント管理人',icon_url=ct.user.avatar.url)
      embed.add_field(name='==========イベント参加登録==========',value='イベントに参加希望の方はボタンを押してください',inline=False)
      await interaction.response.send_message(embed=embed,view=view)
    
    @tree.command(name="chat",description="裏切り烏賊用コマンドです。")
    async def chat_command(interaction: discord.Interaction):
      members = interaction.user.voice.channel.members
      view = ChatButton(timeout=None,members=members,interaction=interaction)
      embed = discord.Embed(color=0xff0000)
      embed.set_author(name='ゲームマスター',icon_url=ct.user.avatar.url)
      embed.add_field(name='==========裏切り命令ボタン==========',value="裏切りものを選べ！",inline=False)
      await interaction.response.send_message(embed=embed,view=view)
    
    
    @tree.command(name="url",description="スプレッドシートのリンク表示用コマンド")
    async def url_command(interaction: discord.Interaction):
      url_txt = "https://docs.google.com/spreadsheets/d/"+SPREADSHEET_KEY+"/edit"
      embed = discord.Embed(title='イベント管理用スプレッドシート',color=0x00ff00,url=url_txt,description='タイトルからイベント管理用スプレッドシートに飛べます。')
      embed.set_author(name='イベント管理人',icon_url=ct.user.avatar.url)
      embed.add_field(name='スプレッドシートで確認できること',value="1.今開催中のイベントの確認\n2.今開催中のイベントの参加状況\n3.ボットが管理していた過去のイベント情報",inline=False)
      await interaction.response.send_message(embed=embed)

    #全てのインタラクションを取得
    @ct.event
    async def on_interaction(inter:discord.Interaction):
      try:
        if inter.data['component_type'] == 2:
          print(inter.data)
        if inter.data['custom_id'] == 'entry_button':
          await on_EntryButton(inter)
        if inter.data['custom_id'] == 'entry_button2':
          await on_EntryButton2(inter)
        if inter.data['custom_id'] == 'point_button_p2':
          await on_point_button_p2(inter)
        if inter.data['custom_id'] == 'point_button_p1':
          await on_point_button_p1(inter)
        if inter.data['custom_id'] == 'point_button_m1':
          await on_point_button_m1(inter)
      except KeyError:
        pass
    
    return ct

# ウェブサーバーを起動する
keep_alive()

#try:
task = BotTask()
task.start_with_retry()
#except:
#  os.system("kill 1")