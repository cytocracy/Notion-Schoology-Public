import notion
import schoology
from objects import Assignment

ass = schoology.get_assignments()[0]
notion.create_assignment(ass)