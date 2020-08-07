import sys
from krwordrank.word import KRWordRank
# from konlpy.tag import Okt // 자바 8 이상 깔려있어야 동작.
import json

# TEST Texts
# texts = [
#     "괜찮은데 이게 집전화 열결이 되있는거라서... 번호가070으로 시작 하거든요... 근데 집전화는 뭐 문자가 못온다고 해서 그게 조금 아쉽고 로그인할때 이메일,비밀번호로만 할수 있게 해주시면 불편한점은 없겠네요...",
#     "배경사진 업로드하면 기존사진 사라지는거 저만 그런가요 ?? 최신버전으로 업데이트 해도 안되는데 저만 그런건가요 ㅜㅜ 예를들어 강아지사진을 배경사진에 등록하고나서 고양이사진을 배경사진으로 올리면 고양이사진이 배경으로 바뀌고 배경사진 목록에 강아지 사진이 있어야되는데 없네오 ㅜㅜ",
#     "지문인식 업데이트되고 나서 한번씩 지문인식창에서 렉이 걸리고 팝업이 계속 뜬채로 안없어져서 계속 다시시작하기를 해야됩니다... 게다가 그렇게 3번정도 반복하다보니 앱에 지문 잠금 기능이 아예 사라졌네요 버그 수정 부탁드립니다",
#     "안녕하세요:3 카카오톡 한유저로써 말합니다:3 카카오톡 옾챗 정지를 당해, 옾챗을 하기 위해 , 그냥 무턱되고 앱을 삭제했습니다. 계정을 찾는다고 지금 쓰는 계정을 여러번 썻습니다:3 그런데 계속 혜당 계속으론 로그인 할 수 없다고 뜹니다. 제가 생각이 없어서 그런지 아니면 그저 옾챗 정지를 당해서 그런지 아무것도 알 수가 없었습니다:3 이 리뷰를 늦게 본다라고 한들, 제발 부탁이니 손 좀 써주셨으면 합니다:3 이상 헛소리 였지만 그래도 답변해주셨으면 합니다:3",
#     "제발 부탁이에요 보이스톡 할 때 네트워크 연결이 불안정하다면서 '띵띵'하는 소리 제발 없애주세요 너무 시끄러워요, 실험실에라도 없앨 수 있는 기능 만들어주세요... 보이스톡 애용하는데 노이로제 걸릴 것 같아요",
#     "다 좋은데 두 가지 점이 너무 아쉬워요... 첫 번째는 프로필에 영화를 올릴 수 있는 기능이 사라진 것, 두 번째는 전송했던 메시지를 아예 삭제하고 싶을 때 자꾸 '내 채팅방에서만 삭제하기'밖에 안 뜨고 '상대방의 채팅방에도 메시지를 삭제하기'가 안 뜨는 오류가 꽤 빈번하게 발생해요 ㅠㅠ 영화는 저작권 때문인지 모르겠지만 원래는 있었던 기능이니 다시 한번 검토해 주시면 감사할 것 같아요...! 그리고 메시지 삭제하기 오류는 왜 자꾸 발생하는지 모르겠지만 이것도 한번 확인해 주시면 감사하겠습니다!!",
#     "다 맘에 들어요 ! ㅠ 근데 딱하나가 아쉬워요 예전에는 오픈채팅카드를 10개 만들수있었는데 이제는 3개밖에 못만든다는게 너무 아쉬워요 ! 혹시 10개는 아니여도 5개 정도로 하면 안될까요 오픈채팅카드가 적어서 많은방에서 다 다른 프로필 카드로 있기가 불편해요 ! 항상 프로필을 다른걸 있던걸 바꾼다는게 너무 힘들고 귀찮아요 ! 2개만 더 늘려주실수있을까요?",
#     "앱 정말 잘쓰고 있습니다. 근데 제가 방금 긴글을 써서 보냈는데 오타가 좀 있어서 다시 쓸려고 했어요. 하지만 삭제하면 다시 써야 하는데 귀찮아서......'수정' 이라는게 있으면 좋을거 같아요.",
#     "그동안 카톡 잘 사용했는데 업데이트 후 생체인증 (지문) 페이지가 별도로 뜨면서 사용하는데 너무 불편해졌습니다.. 지문인식 페이지 뜨고 렉이 걸려서 그 화면이 사라지지 않는 경우가 너무 많이 발생합니다. 진짜.. 그럴때마다 다른거 다 안눌려서 전원 껐다 켜야하는데.. 정말 불편합니다. 예전처럼 지문인식을 카톡 내 화면으로 바꿔주시면 좋겠습니다. 지금 너무 불편해서 그동안 잘 사용하던 지문인식 잠금을 아예 꺼버렸습니다.. 개선 바랍니다.",
#     "잘사용하고 있는데요 오픈채팅방에서 다른분들과 소통하던 도중 이유도 모른체 신고당해서요 한번 여기에 얘기해봅니다 아무잘못도 안했는데 갑자기 옾정이라니 좀 당황스럽네요 하루나 이틀도 아니고 일주일씩이나 정지당하고 반단톡도 오픈채팅방으로 연결되어있어 반단톡도 못하고 있는 상황입니다",
#     "버그가 너무 심해요... 프로필을 GIF로 바꾸는데 갑자기 카톡이 나가지고 덩달아 핸드폰도 이상해지는 경우가 엄청 흔하고...또 오픈채팅방에 알 수 없는 공백이 생기고 스크롤도 안되고.. 또 앱의 캐시랑 데이터는 뭐하는데 몇 기가바이트씩 쓰는거죠..",
#     "아니 친구,동생,형누나랑 보이스톡,페이스톡 할때 검은색화면뜨고 버그가 걸렸군요.... 별 1개주기가 아깝군요......... 개짜증나요 😡 왜그러죠? 그리고 앱누르자마자 검은색화면,튕김이 있어요! 좀 개선하세요!",
#     "요즘 위아래로 긴 사진을 모바일에서 확인하면 맨 밑에 있는 다운로드/전달/삭제/... 버튼이 있는 까만 박스가 사라지질 않아서 내용을 확인하기 힘드네요... 한 번 더 터치하면 사라지게 인터페이스를 바꿔주시면 감사드리겠습니다.",
#     "다좋은데 왜 갑자기 프로필 뮤직을 설정하려면 흰화면만 뜨는 거죠??끄고 다시 켜도 거의 5일째 흰화면만 뜨네요 고쳐주세요ㅜ +)고쳐주셨네열??오올 답답해죽는줄 알았는데 살 것 같아요ㅎㅎ 기시기시~별점 올려드림",
# ]

# texts = sys.stdin.readlines()
# def Keyword(texts): // 자바 8이상 깔려 있어야 동작.
#     extractor = KRWordRank(min_count = 1, max_length = 120)
#     keywords, rank, graph = extractor.extract(texts, beta = 0.85, max_iter = 30)

#     okt = Okt()

#     wanted_pos = ['Noun',]

#     outputs = []
#     for w, r in sorted(keywords.items(), key=lambda x : x[1], reverse=True) :
#         pos = [ n[0] for n in okt.pos(w) if n[1] in wanted_pos ]
#         outputs.extend(pos)

#     print (outputs[:5])

#     jsonData = json.dump(dict( zip(range(SIZE), outputs[:SIZE] ) ),ensure_ascii=False)
#     # SIZE = 5
#     # with open("tagsOfArticle.json", "w") as f:
#     #     json.dump( dict( zip(range(SIZE), outputs[:SIZE] ) ), f, ensure_ascii=False)
#     return jsonData

def mkKeywords (texts) :

    SIZE = 5

    extractor = KRWordRank(min_count = 1, max_length = 120)

    keywords, rank, graph = extractor.extract(texts, beta = 0.85, max_iter = 30)

    outputs = []
    for w, r in sorted(keywords.items(), key=lambda x : x[1], reverse=True) :
        outputs.append(w)
    
    # return json.dumps( dict( zip(range(SIZE), outputs[:SIZE] ) ),ensure_ascii=False)
    return dict( zip(range(SIZE), outputs[:SIZE] ) )