import { Link } from "react-router-dom";


type PaginationProps = {
  pagination: {
    total: number;
    pages: number;
    current_page: number;
  };
  nextPageFunc: (page: number) => void;
};


const PagePagination = ({ pagination, nextPageFunc }: PaginationProps) => {
  return (
    <div className="pagination">
      {/* Prev Button */}
      {pagination.current_page > 1 && (
        <Link to="#" onClick={() => nextPageFunc(pagination.current_page - 1)}>« Prev</Link>
      )}

      {/* Các số trang */}
      {[...Array(pagination.pages)].map((_, idx) => {
        const pageNum = idx + 1;

        // Xác định vị trí trang hiện tại và các trang hiển thị
        const isAdjacent =
          pageNum === pagination.current_page ||
          pageNum === pagination.current_page - 1 ||
          pageNum === pagination.current_page + 1;

        const isEdgePage =
          pageNum === 1 || pageNum === 2 || pageNum === pagination.pages || pageNum === pagination.pages - 1;

        // Kiểm tra xem dấu "..." có nên hiển thị không
        const showEllipsis =
          (pageNum === pagination.current_page - 2 && pagination.current_page > 4) ||
          (pageNum === pagination.current_page + 2 && pagination.current_page < pagination.pages - 3);

        return (
          <>
            {/* Hiển thị dấu ... */}
            {showEllipsis && <span key={`ellipsis-${pageNum}`} className="dots">...</span>}

            {/* Hiển thị các trang */}
            {(isAdjacent || isEdgePage) && (
              <>
                {pageNum === pagination.current_page ? (
                  <span className="current">{pageNum}</span>
                ) : (
                  <a href="#" onClick={() => nextPageFunc(pageNum)}>
                    {pageNum}
                  </a>
                )}
              </>
            )}
          </>
        );
      })}

      {/* Next Button */}
      {pagination.current_page < pagination.pages && (
        <Link to="#" onClick={() => nextPageFunc(pagination.current_page + 1)}>Next »</Link>
      )}
    </div>
  );
}

export default PagePagination;