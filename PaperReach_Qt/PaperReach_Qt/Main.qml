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

        // 2. DER SCHATTEN für das gesamte Fenster
        DropShadow {
            anchors.fill: mainBackground
            horizontalOffset: 0
            verticalOffset: 2
            radius: 12.0
            samples: 25
            color: "#40000000" // Sanfter Schatten
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
                        text: "Generated Queries"
                        color: "#616161"
                    }
                }
            }

            Rectangle { // Rechte Seite
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: "#ffffff"
                border.color: "#e6e6e6"
                radius: 8
            }
        }
    }
}
