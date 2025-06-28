from app import create_app
from app.models.category import SubCategory, Category

app = create_app()

with app.app_context():
    print("=== 현재 DB에 등록된 소분류 목록 ===")
    
    # 모든 소분류 조회
    sub_categories = SubCategory.query.all()
    
    if not sub_categories:
        print("❌ 등록된 소분류가 없습니다.")
    else:
        print(f"총 {len(sub_categories)}개의 소분류가 등록되어 있습니다.\n")
        
        for sub_cat in sub_categories:
            # 대분류 정보도 함께 조회
            category = Category.query.filter_by(category_id=sub_cat.category_id).first()
            category_name = category.name if category else "알 수 없음"
            
            print(f"📂 {sub_cat.name}")
            print(f"   - sub_category_id: '{sub_cat.sub_category_id}'")
            print(f"   - 대분류: {category_name} (category_id: '{sub_cat.category_id}')")
            print(f"   - DB ID: {sub_cat.id}")
            print()
    
    print("=== 대분류 목록 ===")
    categories = Category.query.all()
    
    if not categories:
        print("❌ 등록된 대분류가 없습니다.")
    else:
        print(f"총 {len(categories)}개의 대분류가 등록되어 있습니다.\n")
        
        for cat in categories:
            print(f"📁 {cat.name}")
            print(f"   - category_id: '{cat.category_id}'")
            print(f"   - DB ID: {cat.id}")
            print() 