import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects // WICHTIG für DropShadow in Qt 6

Window {
    id: root
    width: 1100
    height: 800
    visible: true
    title: qsTr("PaperReach")

    // 1. SCHATTEN-SETUP: Fensterhintergrund unsichtbar machen
    color: "transparent"
    flags: Qt.FramelessWindowHint | Qt.Window // Window Hint hinzugefügt, damit es in der Taskleiste bleibt




    // Das Haupt-Container-Rectangle (damit der Schatten Platz hat)
    Rectangle {
        id: mainBackground
        anchors.fill: parent
        anchors.margins: 15 // Platz für den Schatten
        color: "#f5f5f5"    // Hintergrundfarbe der App
        radius: 10

        // titelleiste ist Buggy: ist aber ok für jetzt
        Rectangle {
            id: mainContent
            anchors.fill: parent
            anchors.margins: 0
            color: "#f0f0f0"
            radius: 10

            //  TITELLEISTE
            Rectangle {
                id: titleBar
                width: parent.width
                height: 40
                color: "transparent"
                radius: 10
                anchors.top: parent.top

                // Verhindert, dass die unteren Ecken auch rund sind
                Rectangle {
                    anchors.bottom: parent.bottom
                    width: parent.width
                    height: parent.height / 2
                    color: parent.color
                    z: -1
                }

                //Text {
                //    text: "PaperReach"
                //    color: "white"
                //    anchors.centerIn: parent
                //}

                // Qt 6 DragHandler
                DragHandler {
                    onActiveChanged: if (active) root.startSystemMove()
                }

                // Schließen Button
                //Button {
                //    text: "✕"
                //    anchors.right: parent.right
                //    anchors.verticalCenter: parent.verticalCenter
                //    anchors.rightMargin: 10
                //    width: 30; height: 30
//
                //    onClicked: root.close() // Schließt die Applikation
//
                //    background: Rectangle {
                //        color: parent.down ? "#aa3333" : (parent.hovered ? "#ff4444" : "transparent")
                //        radius: 5
                //    }
                //}
            }
        }

        // Schatten
        DropShadow {
            anchors.fill: mainBackground
            horizontalOffset: 0
            verticalOffset: 2
            radius: 12.0
            samples: 25
            color: "#40000000"
            source: mainBackground
            z: -1 // Hinter dem Inhalt zeichnen
        }

        // --- AB HIER IHR BESTEHENDER CONTENT ---
        RowLayout {
            anchors.fill: parent
            spacing: 15
            anchors.margins: 15

            Rectangle { // Linke Seite
                id: leftPanel
                Layout.preferredWidth: 500
                Layout.fillHeight: true
                color: "#ffffff"
                border.color: "#e6e6e6"
                radius: 8

                ColumnLayout {
                    anchors.top: parent.top
                    anchors.left: parent.left
                    anchors.right: parent.right
                    height: parent.height / 2
                    spacing: 15
                    anchors.margins: 20

                    TextArea {
                        id: inputField
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        placeholderText: "Ihre Notizen hier..."
                        background: Rectangle {
                            color: "#fcfcfc"
                            border.color: inputField.activeFocus ? "#3a86ff" : "#e6e6e6"
                            radius: 4
                        }
                        wrapMode: Text.WordWrap
                    }

                    Button {
                        text: "Search"
                        Layout.fillWidth: true
                        Layout.preferredHeight: 40
                        contentItem: Text {
                            text: parent.text
                            font.weight: Font.DemiBold
                            color: "white"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        background: Rectangle {
                            color: parent.down ? "#2a6edb" : (parent.hovered ? "#4a96ff" : "#3a86ff")
                            radius: 4
                        }
                        onClicked: backend.process_text(inputField.text)
                    }

                    Text {
                        text: "Sources"
                        font.pointSize: 10
                        font.weight: Font.Medium
                        color: "#7f8c8d"
                    }

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 20
                        // blaues Design
                        component BlueCheckBox : CheckBox {
                            id: control
                            indicator: Rectangle {
                                implicitWidth: 20
                                implicitHeight: 20
                                x: control.leftPadding
                                y: parent.height / 2 - height / 2
                                radius: 4
                                border.color: control.checked ? "#3a86ff" : "#e6e6e6"
                                color: control.checked ? "#3a86ff" : "transparent"
                                // Das Häkchen
                                Rectangle {
                                    width: 10
                                    height: 10
                                    x: 5
                                    y: 5
                                    radius: 2
                                    color: "white"
                                    visible: control.checked
                                }
                            }
                        }
                        BlueCheckBox {
                            id: semScol
                            text: "Semantic Scholar"
                            checked: true
                            onCheckedChanged: console.log("Semantic Scholar " + checked)
                        }
                        BlueCheckBox {
                            id: arXiv
                            text: "arXiv"
                            checked: true
                            onCheckedChanged: console.log("arXiv " + checked)
                        }
                    }
                }

                Rectangle { // Links unten
                    anchors.bottom: parent.bottom
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.margins: 10
                    height: parent.height / 2 - 60
                    color: "#f9f9f9"
                    border.color: "#e6e6e6"
                    radius: 8

                    Text {
                        anchors.centerIn: parent
                        text: "Papers found"
                        color: "#616161"
                        visible: paperList.count === 0
                    }

                    ScrollView {
                        anchors.fill: parent
                        anchors.margins: 10
                        ScrollBar.vertical.policy: ScrollBar.AsNeeded

                        ListView {
                            id:paperList
                            spacing: 5
                            model: 10

                            delegate: Text {
                                id: name
                                text: "Bonjour"
                                color: "#3b3939"
                            }
                        }
                    }
                }
            }

            Rectangle { // Rechte Seite
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: "#ffffff"
                border.color: "#e6e6e6"
                radius: 8
                clip: true // WICHTIG: Verhindert, dass Inhalt über die abgerundeten Ecken hinausragt

                ScrollView {
                    anchors.fill: parent
                    anchors.margins: 10
                    ScrollBar.vertical.policy: ScrollBar.AsNeeded

                    ListView {
                        id: resultList
                        spacing: 10
                        model: 10

                        delegate: Rectangle {
                            width: resultList.width
                            height: Math.min(resultList.height / 3, 150) // Max 1/3 der Höhe, aber festes Limit
                            color: "#fcfcfc"
                            border.color: "#eeeeee"
                            radius: 6

                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: 15

                                Text {
                                    font.family: "Helvetica"
                                    text: "Ergebnis Titel #" + (index + 1)
                                    // font.weight: Font.Bold
                                    color: "#333333"
                                }

                                Text {
                                    text: "Hier steht der dynamischer Text. Da das Element scrollbar ist, kannst du beliebig viele dieser Boxen untereinander anzeigen lassen. Hier steht der dynamischer Text. Da das Element scrollbar ist, kannst du beliebig viele dieser Boxen untereinander anzeigen lassen."
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#666666"
                                    elide: Text.ElideRight
                                    maximumLineCount: 3
                                }
                                Text {
                                    font.family: "Helvetica"
                                    text: "BibTeX"
                                    font.weight: Font.StyleItalic
                                    color: "#333333"
                                }
                            }
                        }
                    }
                }
            }

        }
    }
}