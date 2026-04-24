import os
import json
from textwrap import dedent

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import requests

# Read the CSV file
data = pd.read_csv('apps/analysis/data.csv')

TRANSLATIONS = {
    'China': '中国', 'Japan': '日本', 'Korea': '韩国', 'Solid': '纯色', 'Abstract': '抽象',
    'Animal Pattern': '动物纹', 'Argyle': '菱格纹', 'Cable': '绞花', 'Camouflage': '迷彩',
    'Chevron': '人字纹', 'Conversational': '趣味图案', 'Damask': '锦缎纹', 'Diamond': '菱形',
    'Dots': '圆点', 'Ethnical': '民族风', 'Floral': '花卉', 'Geometric': '几何',
    'Gingham Check': '维希格', 'Glen Check': '格伦格', 'Herringbone': '人字呢', 'Houndstooth': '千鸟格',
    'Leaf': '叶纹', 'Miscellaneous': '杂项', 'Ombre': '渐变', 'Other Checks': '其他格纹',
    'Paisley': '佩斯利', 'Plaid': '格子', 'Splattered': '泼墨纹', 'Stripes': '条纹',
    'Tie Dyed Pattern': '扎染纹', 'Tropical': '热带风', 'Wave': '波浪纹', 'Acetate': '醋酸纤维',
    'Acrylic': '腈纶', 'Acrylic-blend': '腈纶-混纺', 'Alpaca': '羊驼毛', 'Alpaca-blend': '羊驼毛-混纺',
    'Angora': '安哥拉毛', 'Angora-blend': '安哥拉毛-混纺', 'Bamboo': '竹纤维', 'Bamboo-blend': '竹纤维-混纺',
    'Bonded': '复合', 'Boucle': '圈圈呢', 'Brushed': '磨毛', 'Burnout': '烂花', 'Canvas': '帆布',
    'Cashmere': '羊绒', 'Cashmere-blend': '羊绒-混纺', 'Cation': '阳离子', 'Challis': '薄斜纹软布',
    'Chambray': '青年布', 'Charmeuse': '缎纹绉绸', 'Chiffon': '雪纺', 'Clip Jacquard': '剪花提花',
    'Corduroy': '灯芯绒', 'Cotton': '棉', 'Cotton-blend': '棉-混纺', 'Crepe': '绉布',
    'Crepe Knit': '绉针织', 'Crepe Satin': '绉缎', 'Crochet': '钩编', 'Crushed': '压皱',
    'Cupro': '铜氨纤维', 'Denim': '牛仔布', 'Dew Drop': '露珠纹', 'Dobby': '多臂织',
    'Dope Dye': '原液染色', 'Embellished': '装饰', 'Embellished Tulle': '装饰薄纱', 'Embossed': '压花',
    'Embroidery': '刺绣', 'Enzyme': '酵素洗', 'Eyelet': '镂空刺绣', 'Flannel': '法兰绒',
    'Flatback Rib': '平纹罗纹', 'Fleece': '抓绒', 'Flocking': '植绒', 'Foil': '烫金',
    'French Terry': '毛圈布', 'Gabardine': '华达呢', 'Gauze': '纱布', 'Georgette': '乔其纱',
    'Glitter': '闪光', 'Hemp': '麻', 'Interlining': '衬布', 'ITY Jersey': 'ITY针织', 'Jacquard': '提花',
    'Jacquard Knit': '提花针织', 'Jersey': '针织汗布', 'Jute': '黄麻', 'Knit': '针织', 'Lace': '蕾丝',
    'Lambswool': '羔羊毛', 'Laminated': '贴膜', 'Leather': '皮革', 'Linen': '亚麻', 'Linen-blend': '亚麻-混纺',
    'Loop Terry': '圈圈毛圈布', 'Low Gauge Knit': '粗针针织', 'Lyocell': '莱赛尔', 'Lyocell-blend': '莱赛尔-混纺',
    'Melton': '麦尔登呢', 'Memory': '记忆布', 'Mercerized': '丝光', 'Mesh': '网布', 'Metallic Yarn': '金属丝',
    'Modal': '莫代尔', 'Modal-blend': '莫代尔-混纺', 'Mohair': '马海毛', 'Nap': '绒面', 'Nylon': '尼龙',
    'Nylon-blend': '尼龙-混纺', 'Organic': '有机', 'Organza': '欧根纱', 'Ottoman': '奥斯曼纹', 'Oxford': '牛津布',
    'Perforated': '冲孔', 'Pima': '匹马棉', 'Pique': '珠地布', 'Plain Weave': '平纹', 'Pleated': '褶皱',
    'Pointelle': '镂空针织', 'Polar Fleece': '摇粒绒', 'Polyethylene': '聚乙烯', 'Polyester': '涤纶',
    'Polyester-blend': '涤纶-混纺', 'Ponte': '罗马布', 'Poplin': '府绸', 'PVC': 'PVC面料', 'PU': 'PU',
    'Quilted': '绗缝', 'Quilted Knit': '绗缝针织', 'Raccoon': '浣熊毛', 'Ramie': '苎麻', 'Rattan': '藤编纹',
    'Rayon': '人造丝', 'Recycled': '再生', 'Reflective': '反光', 'Repellent': '防泼水', 'Rib': '罗纹',
    'Ripstop': '防撕裂', 'Satin': '缎布', 'Scuba': '空气层', 'Seersucker': '泡泡纱', 'Sequin': '亮片',
    'Sherpa': '羊羔绒', 'Silk': '丝', 'Silk-blend': '丝-混纺', 'Single Jersey': '单面针织', 'Slub': '竹节',
    'Space Dye': '段染', 'Stretch': '弹力', 'Suri': '苏里羊驼毛', 'Suede': '麂皮', 'Supima': '苏比马棉',
    'Taffeta': '塔夫绸', 'Terry': '毛圈', 'Thermochromic': '热致变色', 'Tricot': '经编', 'Triacetate': '三醋酸纤维',
    'Tulle': '薄纱', 'Tweed': '粗花呢', 'Twill': '斜纹', 'Tyvek': '特卫强', 'Vegan': '人造',
    'Vegan Fur': '人造毛皮', 'Vegan Leather': '人造皮革', 'Vegan Suede': '人造麂皮', 'Velour': '丝绒针织',
    'Velvet': '天鹅绒', 'Velveteen': '棉绒布', 'Viscose': '粘胶', 'Viscose Rayon': '粘胶人造丝',
    'Viscose Rayon-blend': '粘胶人造丝-混纺', 'Voile': '巴里纱', 'Waffle': '华夫格', 'Wash': '水洗',
    'Washer': '皱洗', 'Water': '防水', 'Waxed': '蜡感', 'Weave': '织物', 'Wicking': '吸湿排汗',
    'Wool': '羊毛', 'Wool-blend': '羊毛-混纺', 'Yarn Dye': '色织', 'blend': '混纺', 'Coated': '涂层',
    'back': '背面', 'front': '正面', 'doubled-sided': '双面', 'doubled': '双面', 'sided': '面'
}
SORTED_PHRASES = sorted(TRANSLATIONS.keys(), key=len, reverse=True)


def bilingual(text):
    if text is None:
        return ''
    text = str(text).strip()
    if not text:
        return ''
    if '(' in text and ')' in text:
        return text
    translated = text
    for phrase in SORTED_PHRASES:
        translated = translated.replace(phrase, TRANSLATIONS[phrase])
    translated = translated.replace('(back)', '(背面)').replace('(front)', '(正面)')
    translated = ' '.join(translated.split())
    return f'{text}({translated})' if translated != text else text

def _normalize_bilingual_value(value):
    if value is None:
        return ''
    value = str(value).strip()
    if not value:
        return ''
    if '(' in value and value.endswith(')'):
        return value.split('(', 1)[0].strip()
    return value


# country data
def country_counts():
    countries = data['country'].astype(str).map(_normalize_bilingual_value)
    counts = countries.value_counts()
    preferred_order = ['China', 'Korea', 'Japan']

    result = []
    seen = set()
    for country in preferred_order:
        count = int(counts.get(country, 0))
        result.append([country, count])
        seen.add(country)

    for country, count in counts.items():
        if country in seen:
            continue
        result.append([country, int(count)])

    return result


def price_predict_options():
    """
    为前端提供价格预测相关下拉选项：种类、国家、图案，以及克重范围。
    所有选项都直接来自当前 data.csv，保证与训练数据一致，减少预测偏差。
    """
    df = data.copy()
    for c in ['category_name', 'country', 'pattern']:
        df[c] = df[c].astype(str)
    df['weight'] = pd.to_numeric(df['weight'], errors='coerce')
    df = df.dropna(subset=['weight'])

    categories = sorted([bilingual(v) for v in df['category_name'].unique().tolist()])
    countries = sorted([bilingual(v) for v in df['country'].unique().tolist()])
    patterns = sorted([bilingual(v) for v in df['pattern'].unique().tolist()])

    weight_min = float(df['weight'].min()) if not df.empty else 0.0
    weight_max = float(df['weight'].max()) if not df.empty else 0.0
    weight_median = float(df['weight'].median()) if not df.empty else 0.0

    return {
        'category_names': categories,
        'countries': countries,
        'patterns': patterns,
        'weight_min': weight_min,
        'weight_max': weight_max,
        'weight_median': weight_median,
    }
# 价格平均值，最大值，最小值，标准差,中位数,众数,方差
def price_statistics():
    stats = {
        'mean': round(data['price'].mean(), 2),
        'max': round(data['price'].max(), 2),
        'min': round(data['price'].min(), 2),
        'std': round(data['price'].std(), 2),
        'median': round(data['price'].median(), 2),
        'mode': round(data['price'].mode()[0], 2),
        'variance': round(data['price'].var(), 2),
    }
    return stats


def _build_data_context(max_items: int = 8) -> str:
    """
    将 data.csv 中的关键信息整理成自然语言上下文，供大模型回答时参考。
    控制条目数量，避免提示过长导致响应变慢或超限。
    """
    df = data.copy()

    stats = price_statistics()

    def _top_values(column: str, k: int = 10):
        if column not in df.columns:
            return []
        series = df[column].astype(str).value_counts().head(k)
        return [f"{bilingual(idx)}({int(cnt)})" for idx, cnt in series.items()]

    top_categories = _top_values('category_name', max_items)
    top_countries = _top_values('country', max_items)
    top_patterns = _top_values('pattern', max_items)

    context = dedent(
        f"""
        这是一个关于布料价格的数据集 data.csv 的关键信息摘要：
        - 价格统计：均值 {stats['mean']}，中位数 {stats['median']}，最小值 {stats['min']}，最大值 {stats['max']}，标准差 {stats['std']}。
        - 主要字段：category_name(面料种类)、country(国家)、pattern(图案)、weight(克重)、price(价格) 等。
        - 最常见的面料种类（名称(出现次数)）：{', '.join(top_categories) or '无数据'}。
        - 最常见的国家：{', '.join(top_countries) or '无数据'}。
        - 最常见的图案类型：{', '.join(top_patterns) or '无数据'}。

        回答用户问题时，请结合以上数据特征进行分析和解释，且需要清晰说明结论只是基于历史数据的统计和建模结果，不代表真实交易价格。
        """
    ).strip()

    return context
# 种类价格箱线图数据
def category_price_boxplot_echarts():
    df=data.copy()
    df['category_name'] = df['category_name'].astype(str)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df.dropna(subset=['price'])
    categories=[]
    box_data=[]
    for cat,group in df.groupby('category_name'):
        prices = group['price'].dropna().values
        if len(prices)==0:
            continue
        q1=float(np.percentile(prices,25))
        q2 = float(np.percentile(prices, 50))  # median
        q3 = float(np.percentile(prices, 75))
        mini = float(np.min(prices))
        maxi = float(np.max(prices))
        categories.append(bilingual(cat))
        box_data.append([mini, q1, q2, q3, maxi])
    return {
        "xAxis": categories,
        "data": box_data
    }
# 图案价格箱线图数据
def pattern_price_boxplot_echarts():
    df=data.copy()
    df['pattern'] = df['pattern'].astype(str)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df.dropna(subset=['price'])
    categories=[]
    box_data=[]
    for pat,group in df.groupby('pattern'):
        prices = group['price'].dropna().values
        if len(prices)==0:
            continue
        q1=float(np.percentile(prices,25))
        q2 = float(np.percentile(prices, 50))  # median
        q3 = float(np.percentile(prices, 75))
        mini = float(np.min(prices))
        maxi = float(np.max(prices))
        categories.append(bilingual(pat))
        box_data.append([mini, q1, q2, q3, maxi])
    return {
        "xAxis": categories,
        "data": box_data
    }
# 聚类分析（KMeans）
def clustering_analysis(k=None,k_min=2,k_max=6,topn_cat=5,random_state=42):
    work = data.copy()
    # 类型与清洗
    for c in ['category_name','country','pattern']:
        work[c] = work[c].astype(str)
    for c in ['category_id','weight','price']:
        work[c] = pd.to_numeric(work[c], errors='coerce')
    # 丢弃关键数值缺失
    work = work.dropna(subset=['category_id','weight','price']).reset_index(drop=True)
    # -------- 特征工程：One-Hot + 数值拼接 --------
    cat_cols = ['category_name','country','pattern']
    num_cols = ['category_id','weight','price']   # 将 price 也作为聚类特征，体现“高/中/低价”分层

     # One-Hot 编码（dense，便于后续处理；数据量很大时可改用稀疏）
    ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    # ohe = OneHotEncoder(handle_unknown='ignore', sparse=False)
    ct = ColumnTransformer(
        transformers=[
            ('cat', ohe, cat_cols),
            ('num', 'passthrough', num_cols)
        ]
    )
    # 标准化（对稀疏矩阵请用 with_mean=False，这里是dense）
    scaler = StandardScaler()

    prep = Pipeline(steps=[
        ('ct', ct),
        ('scaler', scaler),
    ])
    X = prep.fit_transform(work[cat_cols + num_cols])
    # -------- 选择最佳 k（如未指定）--------
    chosen_k = k
    sil_map = {}
    if chosen_k is None:
        best_score, best_k = -1, None
        for kk in range(max(2, k_min), max(k_min, k_max) + 1):
            km = KMeans(n_clusters=kk, random_state=random_state, n_init=10)
            labels = km.fit_predict(X)
            score = silhouette_score(X, labels) if len(set(labels)) > 1 else -1
            sil_map[kk] = float(score)
            if score > best_score:
                best_score, best_k = score, kk
        chosen_k = best_k if best_k is not None else 3
    # -------- 最终聚类 --------
    kmeans = KMeans(n_clusters=chosen_k, random_state=random_state, n_init=10)
    clusters = kmeans.fit_predict(X)

    # -------- PCA 2D 用于可视化 --------
    pca = PCA(n_components=2, random_state=random_state)
    coords = pca.fit_transform(X)

    work['cluster'] = clusters
    work['_pc1'] = coords[:, 0]
    work['_pc2'] = coords[:, 1]

    # -------- 簇规模柱状图数据 --------
    size_series = work['cluster'].value_counts().sort_index()
    cluster_labels = [f'Cluster {i} / 簇 {i}' for i in size_series.index.tolist()]
    cluster_sizes = size_series.values.tolist()

    cluster_size_bar = {
        'x': cluster_labels,
        'y': cluster_sizes
    }

    # -------- PCA 散点：按簇输出 ECharts series --------
    pca_series = []
    for c_id in sorted(work['cluster'].unique()):
        sub = work[work['cluster'] == c_id]
        # data: [[x, y, id, title], ...]（id/title 可能为空）
        points = []
        for _, row in sub.iterrows():
            meta = {
                'id': row['id'] if 'id' in work.columns else None,
                'title': bilingual(row['title']) if 'title' in work.columns else None,
                'category': bilingual(row['category_name']),
                'country': bilingual(row['country']),
                'pattern': bilingual(row['pattern']),
                'price': float(row['price']),
                'weight': float(row['weight'])
            }
            points.append([float(row['_pc1']), float(row['_pc2']), meta])

        pca_series.append({
            'name': f'Cluster {c_id} / 簇 {c_id}',
            'type': 'scatter',
            'data': points
        })

    pca_scatter = {
        'legend': [s['name'] for s in pca_series],
        'xName': 'PC1',
        'yName': 'PC2',
        'series': pca_series
    }

    # -------- 每簇画像：数值均值 + 类别Top特征 --------
    # 解出编码后的特征名，找回哪些是数值列、哪些是类别列
    cat_feature_names = list(prep.named_steps['ct'].named_transformers_['cat'].get_feature_names_out(cat_cols))
    num_feature_names = num_cols[:]  # 原始数值列名
    feature_names = cat_feature_names + num_feature_names

    # 反标准化地做"画像"：用原表直接 groupby 均值（数值列）
    profiles = []
    for c_id in sorted(work['cluster'].unique()):
        sub = work[work['cluster'] == c_id]
        # 数值画像
        num_profile = {
            'price_mean': float(sub['price'].mean()),
            'weight_mean': float(sub['weight'].mean()),
            'category_id_mean': float(sub['category_id'].mean())
        }
        # 类别Top（统计占比靠前的类别）
        top_categories = sub['category_name'].value_counts(normalize=True).head(topn_cat)
        top_patterns  = sub['pattern'].value_counts(normalize=True).head(topn_cat)
        top_countries = sub['country'].value_counts(normalize=True).head(topn_cat)

        profiles.append({
            'cluster': int(c_id),
            'size': int(len(sub)),
            'numeric_profile': num_profile,
            'top_category_name': [[bilingual(k), float(v)] for k, v in top_categories.items()],
            'top_pattern': [[bilingual(k), float(v)] for k, v in top_patterns.items()],
            'top_country': [[bilingual(k), float(v)] for k, v in top_countries.items()],
        })

    # -------- 明细（可选）：返回 id、title、cluster --------
    assignments_cols = [c for c in ['id','title','cluster','category_name','country','pattern','weight','price'] if c in work.columns]
    assignments = work[assignments_cols].copy()
    for col in ['title', 'category_name', 'country', 'pattern']:
        if col in assignments.columns:
            assignments[col] = assignments[col].map(bilingual)
    # 转为 list[dict] 便于前端直接渲染
    assignments = assignments.to_dict(orient='records')

    # -------- 结果组装（给 ECharts/前端） --------
    result = {
        'k': int(chosen_k),
        'silhouette': sil_map,   # 若自动选 k，这里有各 k 的分数
        'pca_scatter': pca_scatter,
        'cluster_size_bar': cluster_size_bar,
        'cluster_profiles': profiles,
        'assignments': assignments
    }
    return result
def price_prediction_model(test_size=0.2, random_state=42):
    # 1) 读取与清洗
    df = data.copy()
    cols = ['category_name','category_id','weight','country','pattern','price']
    for c in ['category_name','country','pattern']:
        df[c] = df[c].astype(str)
    for c in ['category_id','weight','price']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df = df[cols].dropna().reset_index(drop=True)

    # 2) 特征/目标
    X = df[['category_name','weight','country','pattern']]
    # X = df[['category_name','category_id','weight','country','pattern']]
    y = df['price']
    categorical = ['category_name','country','pattern']
    numeric = ['weight']
    # numeric = ['category_id','weight']

    ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', ohe, categorical),
            ('num', 'passthrough', numeric)
        ]
    )

    # 3) 划分训练/测试
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # 4) 线性回归
    linear_model = Pipeline(steps=[
        ('preprocess', preprocessor),
        ('model', LinearRegression())
    ])
    linear_model.fit(X_train, y_train)
    y_pred_lin = linear_model.predict(X_test)
    lin_r2 = float(r2_score(y_test, y_pred_lin))
    lin_rmse = float(np.sqrt(mean_squared_error(y_test, y_pred_lin)))
    # lin_rmse = float(mean_squared_error(y_test, y_pred_lin, squared=False))

    # 5) 随机森林
    rf_model = Pipeline(steps=[
        ('preprocess', preprocessor),
        ('model', RandomForestRegressor(n_estimators=300, random_state=random_state))
    ])
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    rf_r2 = float(r2_score(y_test, y_pred_rf))
    rf_rmse = float(mean_squared_error(y_test, y_pred_rf))

    # 6) 特征重要性（One-Hot 后的列名）
    ohe_fitted = rf_model.named_steps['preprocess'].named_transformers_['cat']
    feature_names = list(ohe_fitted.get_feature_names_out(categorical)) + numeric
    importances = rf_model.named_steps['model'].feature_importances_
    feat_imp_sorted = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)

    # 7) ECharts 数据：实际 vs 预测 散点（两模型）
    echarts_scatter = {
        "xName": "Actual Price",
        "yName": "Predicted Price",
        "series": {
            "LinearRegression": [[float(a), float(p)] for a, p in zip(y_test.tolist(), y_pred_lin.tolist())],
            "RandomForest": [[float(a), float(p)] for a, p in zip(y_test.tolist(), y_pred_rf.tolist())]
        }
    }

    # 8) ECharts 数据：特征重要性柱状
    echarts_importance = {
        "features": [f for f, _ in feat_imp_sorted],
        "importance": [float(v) for _, v in feat_imp_sorted]
    }

    result = {
        "linear_metrics": {"R2": lin_r2, "RMSE": lin_rmse},
        "rf_metrics": {"R2": rf_r2, "RMSE": rf_rmse},
        "echarts": {
            "scatter_pred_vs_actual": echarts_scatter,
            "bar_feature_importance": echarts_importance
        }
    }
    return result
PRICE_PREDICTION = price_prediction_model()

# 全局缓存训练好的模型，避免每次预测都重新训练
_CACHED_PREDICTION_MODEL = None
_CACHED_WEIGHT_RANGE = None

def _get_or_train_prediction_model():
    """
    获取或训练预测模型（单例模式）。
    只在第一次调用时训练，后续直接返回缓存的模型。
    """
    global _CACHED_PREDICTION_MODEL, _CACHED_WEIGHT_RANGE
    
    if _CACHED_PREDICTION_MODEL is not None:
        return _CACHED_PREDICTION_MODEL, _CACHED_WEIGHT_RANGE
    
    # 训练模型
    df = data.copy()
    cols = ['category_name','category_id','weight','country','pattern','price']
    for c in ['category_name','country','pattern']:
        df[c] = df[c].astype(str)
    for c in ['category_id','weight','price']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df = df[cols].dropna().reset_index(drop=True)

    if df.empty:
        raise ValueError("训练数据为空，无法进行价格预测")

    X = df[['category_name','weight','country','pattern']]
    y = df['price']
    categorical = ['category_name','country','pattern']
    numeric = ['weight']

    # 训练随机森林模型（全量数据）
    ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', ohe, categorical),
            ('num', 'passthrough', numeric)
        ]
    )
    rf_model = Pipeline(steps=[
        ('preprocess', preprocessor),
        ('model', RandomForestRegressor(n_estimators=120, max_depth=16, min_samples_leaf=2, n_jobs=-1, random_state=42))
    ])
    rf_model.fit(X, y)
    
    # 缓存权重范围
    weight_range = {
        'min': float(df['weight'].min()),
        'max': float(df['weight'].max())
    }
    
    _CACHED_PREDICTION_MODEL = rf_model
    _CACHED_WEIGHT_RANGE = weight_range
    
    return rf_model, weight_range

def predict_single_price(category_name, country, pattern, weight, random_state=42):
    """
    根据单条记录的特征预测价格。
    使用缓存的模型进行预测，避免每次都重新训练。
    """
    # 获取缓存的模型
    rf_model, weight_range = _get_or_train_prediction_model()
    
    # 将传入的 weight 限制在训练数据范围内，避免极端外推导致偏差过大
    w_value = float(weight)
    if w_value < weight_range['min']:
        w_value = weight_range['min']
    if w_value > weight_range['max']:
        w_value = weight_range['max']

    sample = pd.DataFrame([{
        'category_name': str(category_name),
        'country': str(country),
        'pattern': str(pattern),
        'weight': w_value,
    }])
    pred = rf_model.predict(sample)[0]
    return float(pred)


def ai_answer_with_data(
    question: str,
    enable_web_search: bool = False,
    enable_deep_thinking: bool = False,
) -> str:
    """
    调用外部大模型接口，结合本地 data.csv 摘要进行问答。

    - 默认使用 DeepSeek Chat 作为基础模型；
    - 当 enable_deep_thinking=True 时，切换为 DeepSeek Reasoner 模型；
    - 当 enable_web_search=True 时，打开联网搜索工具（如果模型支持）。
    """
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        return "后端未配置大模型 API Key（环境变量 DEEPSEEK_API_KEY），暂时无法调用 AI 问答功能，请联系管理员。"

    system_context = _build_data_context()

    model = "deepseek-reasoner" if enable_deep_thinking else "deepseek-chat"

    # DeepSeek 官方 HTTP 接口
    url = "https://api.deepseek.com/v1/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "你是一名专注于布料价格分析与预测的智能助手。"
                    "优先使用我提供的数据摘要进行推理；当用户问题超出数据范围时，可以结合通用行业知识做出合理解释。"
                    "回答时用简体中文，结构清晰、有条理。"
                ),
            },
            {"role": "system", "content": system_context},
            {
                "role": "user",
                "content": question,
            },
        ],
    }

    # 联网搜索功能（如果 DeepSeek 支持）
    if enable_web_search:
        payload["web_search"] = True

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        
        # 如果是 401 错误，返回更详细的错误信息
        if resp.status_code == 401:
            return "API Key 认证失败（401 错误）。请检查：1) API Key 是否正确；2) API Key 是否已激活；3) 账户是否有余额。请访问 https://platform.deepseek.com/ 检查您的 API Key。"
        
        resp.raise_for_status()
        data_json = resp.json()

        try:
            content = data_json["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            # 兜底，保证前端始终拿到可展示的信息
            content = "大模型接口返回格式异常，请稍后重试或联系管理员检查后端日志。"
            
    except requests.exceptions.RequestException as e:
        return f"调用 DeepSeek API 失败：{str(e)}。请检查网络连接和 API Key 配置。"

    return content


def ai_answer_with_data_stream(
    question: str,
    enable_web_search: bool = False,
    enable_deep_thinking: bool = False,
):
    """
    调用外部大模型接口，结合本地 data.csv 摘要进行问答（流式输出）。
    """
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        yield "后端未配置大模型 API Key（环境变量 DEEPSEEK_API_KEY），暂时无法调用 AI 问答功能，请联系管理员。"
        return

    system_context = _build_data_context()

    model = "deepseek-reasoner" if enable_deep_thinking else "deepseek-chat"

    # DeepSeek 官方 HTTP 接口
    url = "https://api.deepseek.com/v1/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "你是一名专注于布料价格分析与预测的智能助手。"
                    "优先使用我提供的数据摘要进行推理；当用户问题超出数据范围时，可以结合通用行业知识做出合理解释。"
                    "回答时用简体中文，结构清晰、有条理。"
                ),
            },
            {"role": "system", "content": system_context},
            {
                "role": "user",
                "content": question,
            },
        ],
        "stream": True,  # 启用流式输出
    }

    # 联网搜索功能（如果 DeepSeek 支持）
    if enable_web_search:
        payload["web_search"] = True

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=120, stream=True)
        
        # 如果是 401 错误，返回更详细的错误信息
        if resp.status_code == 401:
            yield "API Key 认证失败（401 错误）。请检查：1) API Key 是否正确；2) API Key 是否已激活；3) 账户是否有余额。请访问 https://platform.deepseek.com/ 检查您的 API Key。"
            return
        
        resp.raise_for_status()

        # 逐行读取流式响应
        for line in resp.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data_str = line_str[6:]
                    if data_str == '[DONE]':
                        break
                    try:
                        data_json = json.loads(data_str)
                        delta = data_json.get("choices", [{}])[0].get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            yield content
                    except json.JSONDecodeError:
                        continue
            
    except requests.exceptions.RequestException as e:
        yield f"调用 DeepSeek API 失败：{str(e)}。请检查网络连接和 API Key 配置。"

    return content


# PRICE_PREDICTION = None
if __name__ == "__main__":
    # print(category_price_boxplot_echarts())
    print(price_prediction_model())