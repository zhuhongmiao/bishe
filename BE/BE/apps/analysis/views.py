from django.views.decorators.csrf import csrf_exempt
import json

import apps.analysis.utils as u
from utils.responseMessage import ResponseMessage


def get_countries(request):
    data = u.country_counts()
    return ResponseMessage.success(data)


def price_statistics(request):
    data = u.price_statistics()
    return ResponseMessage.success(data)


def price_predict_options(request):
    """
    提供价格预测下拉所需的选项数据，全部来自 data.csv，
    保证与训练数据一致，减少预测偏差。
    """
    data = u.price_predict_options()
    return ResponseMessage.success(data)


def category_price_boxplot_echarts(request):
    data = u.category_price_boxplot_echarts()
    return ResponseMessage.success(data)


def pattern_price_boxplot_echarts(request):
    data = u.pattern_price_boxplot_echarts()
    return ResponseMessage.success(data)


def clustering_analysis(request):
    k = request.GET.get('k')
    k_min = request.GET.get('k_min', 2)
    k_max = request.GET.get('k_max', 6)
    topn_cat = request.GET.get('topn_cat', 5)
    random_state = request.GET.get('random_state', 42)
    if k is not None:
        k = int(k)
    result = u.clustering_analysis(
        k=k,
        k_min=int(k_min),
        k_max=int(k_max),
        topn_cat=int(topn_cat),
        random_state=int(random_state),
    )
    return ResponseMessage.success(result)


def price_prediction_model(request):
    # test_size = float(request.GET.get('test_size', 0.2))
    # random_state = int(request.GET.get('random_state', 42))
    # result = u.price_prediction_model(test_size=test_size, random_state=random_state)
    # return ResponseMessage.success(result)
    return ResponseMessage.success(u.PRICE_PREDICTION)


@csrf_exempt
def price_predict_single(request):
    if request.method != 'POST':
        return ResponseMessage.failed("仅支持 POST 请求")

    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return ResponseMessage.failed("请求体不是有效的 JSON")

    category_name = body.get("category_name")
    country = body.get("country")
    pattern = body.get("pattern")
    weight = body.get("weight")

    if not category_name or not country or not pattern or weight is None:
        return ResponseMessage.failed("缺少必填字段")

    try:
        weight_value = float(weight)
    except (TypeError, ValueError):
        return ResponseMessage.failed("weight 必须为数字")

    try:
        price = u.predict_single_price(category_name, country, pattern, weight_value)
    except Exception as e:
        return ResponseMessage.failed(f"价格预测失败: {e}")

    return ResponseMessage.success({"price": price})


@csrf_exempt
def ai_chat_with_data(request):
    """
    AI 问答接口：结合 data.csv 数据，并支持联网搜索与深度思考开关。
    """
    if request.method != "POST":
        return ResponseMessage.failed("仅支持 POST 请求")

    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return ResponseMessage.failed("请求体不是有效的 JSON")

    question = body.get("question", "").strip()
    enable_web_search = bool(body.get("enable_web_search", False))
    enable_deep_thinking = bool(body.get("enable_deep_thinking", False))

    if not question:
        return ResponseMessage.failed("问题不能为空")

    try:
        answer = u.ai_answer_with_data(
            question=question,
            enable_web_search=enable_web_search,
            enable_deep_thinking=enable_deep_thinking,
        )
    except Exception as exc:
        return ResponseMessage.failed(f"AI 问答失败: {exc}")

    return ResponseMessage.success({"answer": answer})


@csrf_exempt
def ai_chat_with_data_stream(request):
    """
    AI 问答流式接口：结合 data.csv 数据，支持流式输出。
    """
    if request.method != "POST":
        return ResponseMessage.failed("仅支持 POST 请求")

    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return ResponseMessage.failed("请求体不是有效的 JSON")

    question = body.get("question", "").strip()
    enable_web_search = bool(body.get("enable_web_search", False))
    enable_deep_thinking = bool(body.get("enable_deep_thinking", False))

    if not question:
        return ResponseMessage.failed("问题不能为空")

    def event_stream():
        try:
            for chunk in u.ai_answer_with_data_stream(
                question=question,
                enable_web_search=enable_web_search,
                enable_deep_thinking=enable_deep_thinking,
            ):
                yield f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as exc:
            yield f"data: {json.dumps({'error': str(exc)}, ensure_ascii=False)}\n\n"

    from django.http import StreamingHttpResponse
    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response