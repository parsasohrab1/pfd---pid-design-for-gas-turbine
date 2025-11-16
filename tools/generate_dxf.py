import os
from pathlib import Path

import ezdxf
from ezdxf.entities import Text
from ezdxf.enums import TextEntityAlignment


OUTPUT_DIR = Path(__file__).resolve().parent.parent / "cad"


def _place_text(text_entity: Text, pos: tuple[float, float], center: bool = False) -> None:
	"""
	Compatibility helper for ezdxf versions that may not support Text.set_pos.
	Positions text at pos, with optional center alignment if supported.
	"""
	try:
		# Prefer modern API if available
		if hasattr(text_entity, "set_pos"):
			align = TextEntityAlignment.MIDDLE_CENTER if center else TextEntityAlignment.LEFT
			text_entity.set_pos(pos, align=align)  # type: ignore[attr-defined]
			return
	except Exception:
		pass

	# Fallback: basic insert point (no alignment guarantees)
	text_entity.dxf.insert = pos
	# Best-effort center hint for some versions
	if center and hasattr(text_entity.dxf, "halign") and hasattr(text_entity.dxf, "valign"):
		try:
			text_entity.dxf.halign = 1  # center
			text_entity.dxf.valign = 1  # middle
		except Exception:
			pass


def add_title(msp, title: str, x: float, y: float):
	"""
	Draws a centered title text at (x, y).
	"""
	t = msp.add_text(
		title,
		dxfattribs={"height": 10},
	)
	_place_text(t, (x, y), center=True)


def add_box(msp, insert, size, text: str):
	"""
	Draws a labeled rectangle.
	insert: (x, y) lower-left
	size: (w, h)
	text: centered label
	"""
	x, y = insert
	w, h = size
	msp.add_lwpolyline([(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)], dxfattribs={"closed": True})
	t = msp.add_text(text, dxfattribs={"height": 4})
	_place_text(t, (x + w / 2, y + h / 2), center=True)


def add_conn(msp, p1, p2, label: str | None = None, arrow: bool = False):
	"""
	Draws a connection line from p1 to p2 with optional label and arrowhead.
	"""
	msp.add_line(p1, p2)
	if arrow:
		# simple arrowhead
		ax, ay = p2
		msp.add_solid([(ax, ay), (ax - 2, ay - 1), (ax - 2, ay + 1)])
	if label:
		lx = (p1[0] + p2[0]) / 2
		ly = (p1[1] + p2[1]) / 2 + 2
		t = msp.add_text(label, dxfattribs={"height": 3})
		_place_text(t, (lx, ly), center=True)


def generate_pfd(path: Path):
	doc = ezdxf.new(setup=True)
	msp = doc.modelspace()
	add_title(msp, "PFD — Fuel System (Siemens SGT600/IGT25)", 150, 190)

	# Row 1: Inlet → Filter → KO → Heater
	add_box(msp, (20, 160), (40, 20), "Fuel Gas\nSupply\n(20–70 barg)")
	add_box(msp, (80, 160), (40, 20), "Filter/\nCoalescer")
	add_box(msp, (140, 160), (40, 20), "KO Drum")
	add_box(msp, (200, 160), (40, 20), "Conditioning/\nHeater\n(if req.)")
	add_conn(msp, (60, 170), (80, 170), None, arrow=True)
	add_conn(msp, (120, 170), (140, 170), None, arrow=True)
	add_conn(msp, (180, 170), (200, 170), None, arrow=True)

	# Split to Primary/Main
	add_box(msp, (120, 120), (40, 20), "TEE Split")
	add_conn(msp, (220, 170), (220, 130), None)
	add_conn(msp, (220, 130), (160, 130), None, arrow=True)

	# Primary branch
	add_box(msp, (40, 80), (50, 20), "SDV-PR-001")
	add_box(msp, (100, 80), (50, 20), "FT-PR-010")
	add_box(msp, (160, 80), (60, 20), "FCV-PR-101\n(Actuator Ex)")
	add_conn(msp, (140, 130), (65, 130), "Primary", False)
	add_conn(msp, (65, 130), (65, 100), None)
	add_conn(msp, (65, 100), (65, 90), None, arrow=True)
	add_conn(msp, (90, 90), (100, 90), None, arrow=True)
	add_conn(msp, (150, 90), (160, 90), None, arrow=True)

	# Main branch
	add_box(msp, (40, 40), (50, 20), "SDV-MN-001")
	add_box(msp, (100, 40), (50, 20), "FT-MN-020")
	add_box(msp, (160, 40), (60, 20), "FCV-MN-201\n(Actuator Ex)")
	add_conn(msp, (160, 130), (65, 130), "Main", False)
	add_conn(msp, (160, 130), (160, 60), None)
	add_conn(msp, (65, 60), (65, 50), None, arrow=True)
	add_conn(msp, (90, 50), (100, 50), None, arrow=True)
	add_conn(msp, (150, 50), (160, 50), None, arrow=True)

	# Mixing Header to GT
	add_box(msp, (240, 60), (60, 60), "Mixing Header\nPT-002")
	add_conn(msp, (220, 90), (240, 90), None, arrow=True)
	add_conn(msp, (220, 50), (240, 50), None, arrow=True)
	add_conn(msp, (300, 90), (330, 90), "To GT Combustion", True)

	# Measurements (conceptual callouts)
	t1 = msp.add_text("PT-001 @ Filter Outlet", dxfattribs={"height": 3})
	_place_text(t1, (95, 185))
	t2 = msp.add_text("TT-001 @ KO Outlet", dxfattribs={"height": 3})
	_place_text(t2, (155, 185))

	doc.saveas(str(path))


def generate_pid(path: Path):
	doc = ezdxf.new(setup=True)
	msp = doc.modelspace()
	add_title(msp, "P&ID — Fuel System (Siemens SGT600/IGT25)", 150, 190)

	# Supply block
	add_box(msp, (20, 160), (40, 20), "Fuel Inlet")
	add_box(msp, (70, 160), (40, 20), "Filter/\nCoalescer")
	add_box(msp, (120, 160), (40, 20), "KO Drum")
	add_conn(msp, (60, 170), (70, 170), None, arrow=True)
	add_conn(msp, (110, 170), (120, 170), None, arrow=True)

	# PT/TT upstream
	tpt = msp.add_text("PT-001", dxfattribs={"height": 3})
	_place_text(tpt, (95, 185), center=True)
	ttt = msp.add_text("TT-001", dxfattribs={"height": 3})
	_place_text(ttt, (135, 185), center=True)

	# Split
	add_box(msp, (180, 160), (40, 20), "TEE Split")
	add_conn(msp, (160, 170), (180, 170), None, arrow=True)

	# Primary line with SOV, SDV, FT, FCV, LS
	add_box(msp, (40, 110), (35, 18), "SOV-PR-1\n(Fail Close)")
	add_box(msp, (80, 110), (45, 18), "SDV-PR-001")
	add_box(msp, (130, 110), (45, 18), "FT-PR-010")
	add_box(msp, (180, 110), (60, 18), "FCV-PR-101\nPositioner + LS(O/C)")
	add_conn(msp, (200, 170), (200, 119), "Primary", False)
	add_conn(msp, (200, 119), (57, 119), None, arrow=True)
	add_conn(msp, (75, 119), (80, 119), None, arrow=True)
	add_conn(msp, (125, 119), (130, 119), None, arrow=True)
	add_conn(msp, (175, 119), (180, 119), None, arrow=True)

	# Main line with SOV, SDV, FT, FCV, LS
	add_box(msp, (40, 70), (35, 18), "SOV-MN-1\n(Fail Close)")
	add_box(msp, (80, 70), (45, 18), "SDV-MN-001")
	add_box(msp, (130, 70), (45, 18), "FT-MN-020")
	add_box(msp, (180, 70), (60, 18), "FCV-MN-201\nPositioner + LS(O/C)")
	add_conn(msp, (200, 170), (200, 79), "Main", False)
	add_conn(msp, (200, 79), (57, 79), None, arrow=True)
	add_conn(msp, (75, 79), (80, 79), None, arrow=True)
	add_conn(msp, (125, 79), (130, 79), None, arrow=True)
	add_conn(msp, (175, 79), (180, 79), None, arrow=True)

	# Header and PT-002
	add_box(msp, (260, 80), (60, 60), "Mixing Header")
	tpt2 = msp.add_text("PT-002", dxfattribs={"height": 3})
	_place_text(tpt2, (290, 145), center=True)
	add_conn(msp, (240, 119), (260, 119), None, arrow=True)
	add_conn(msp, (240, 79), (260, 79), None, arrow=True)
	add_conn(msp, (320, 110), (350, 110), "To GT", True)

	# Control/Safety callouts
	c1 = msp.add_text("AO: FCV-PR/MN-Command", dxfattribs={"height": 3})
	_place_text(c1, (60, 30))
	c2 = msp.add_text("DO: SDV Close/Open, SOV Trip", dxfattribs={"height": 3})
	_place_text(c2, (60, 24))
	c3 = msp.add_text("DI: LS Open/Close, Trip Status", dxfattribs={"height": 3})
	_place_text(c3, (60, 18))

	doc.saveas(str(path))


def main():
	OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
	pfd_path = OUTPUT_DIR / "PFD_SGT600_Fuel_Control.dxf"
	pid_path = OUTPUT_DIR / "PID_SGT600_Fuel_Control.dxf"
	generate_pfd(pfd_path)
	generate_pid(pid_path)
	print(f"Generated:\n - {pfd_path}\n - {pid_path}")


if __name__ == "__main__":
	main()


