import "../css/Course.css"

function Course({ course }) {
    return (
        <div className="course-content">
            <div className="course-title-bar">
                <h2 className="course-title">{course.title}</h2>
                <button><a href={course.url}>Go to Course</a></button>
            </div>
            <div className="course-info">
                <p className="course-description">{course.description}</p>
            </div>
        </div>
    );
}

export default Course